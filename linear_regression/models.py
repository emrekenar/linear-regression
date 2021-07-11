import matplotlib

matplotlib.use('Agg')  # this is required for the program to work in OSX

import matplotlib.pyplot as plt
import numpy as np
import io
import urllib
import base64

from random import randint
from django.db import models
from django.utils import timezone


class GradientDescent(models.Model):
    """
    use gradient descent algorithm for linear regression.
    for points (xi, yi), define error function J(theta0, theta1),
    find theta0, theta1 that minimizes J.
    """
    points_x = models.CharField(max_length=200, default='')
    points_y = models.CharField(max_length=200, default='')
    pub_date = models.DateTimeField(default=timezone.now, null=True)
    alpha = models.FloatField(default=0.0)
    acceptable_range = models.FloatField(default=0.0)
    max_steps = models.IntegerField(default=0)
    theta0 = models.FloatField(default=0.0)
    theta1 = models.FloatField(default=0.0)
    error = models.FloatField(default=0.0)

    def init_parameters(self):
        # define points randomly  # TODO: allow users to define points
        sz, min_val, max_val = 10, 0, 10
        points = []
        for i in range(sz):
            points.append(Point(randint(min_val, max_val), randint(min_val, max_val)))
        self.points_x, self.points_y = serialize_points(points)

        # store time of creation  # TODO: make here last edit time and clean unused objects
        self.pub_date = timezone.now()

        # find minimum and maximum values of y
        min_y, max_y = 1024, -1024
        for point in points:
            y = point.y
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        # TODO: compare fixed alpha with a decaying alpha. find a way to calculate best alpha.
        self.alpha = 0.025

        # select a little acceptable range for high precision
        self.acceptable_range = 2 ** -32

        # avoid overflow
        self.max_steps = 1000

        # set initial theta0, theta1 and find error
        self.theta0 = min_y
        self.theta1 = 0.0
        self.error = j(self.theta0, self.theta1, points)

        # save changes to the database
        self.save()

    def proceed(self):
        points = deserialize_points(self.points_x, self.points_y)
        temp = self.theta0 - self.alpha * delta_j(self.theta0, self.theta1, points, 0)
        self.theta1 = self.theta1 - self.alpha * delta_j(self.theta0, self.theta1, points, 1)
        self.theta0 = temp
        self.error = j(self.theta0, self.theta1, points)
        self.save()

    def run(self):
        step = 0
        points = deserialize_points(self.points_x, self.points_y)

        while self.error > self.acceptable_range and step < self.max_steps:
            temp = self.theta0 - self.alpha * delta_j(self.theta0, self.theta1, points, 0)
            self.theta1 = self.theta1 - self.alpha * delta_j(self.theta0, self.theta1, points, 1)
            self.theta0 = temp
            step += 1

        self.error = j(self.theta0, self.theta1, points)
        self.save()

    def get_gd_plot_uri(self):
        """
        create a graph that shows real data, polyfit line and gradient descent fit at each step,
        GD fit is expected to get closer to polyfit as the algorithm proceeds.
        """
        points = deserialize_points(self.points_x, self.points_y)
        x = [p.x for p in points]
        y = [p.y for p in points]

        slope, intercept = np.polyfit(x, y, 1)
        plt_values = [slope * i + intercept for i in x]         # get np.polyfit estimation
        gd_values = [self.theta0 + self.theta1 * i for i in x]  # get gradient descent estimation

        plt.plot(x, y, 'ro')           # denote points by red dots
        plt.plot(x, plt_values, '--')  # denote np.polyfit by a dashed line
        plt.plot(x, gd_values, 'b')    # denote gradient descent fit by a straight line
        plt.legend(["data", "polyfit", "GD fit"], loc="lower right")
        plt.title('np.polyfit vs gradient descent fit')

        return fig_to_uri()

    def get_j_theta_plot_uri(self, index):
        """
        create a graph that shows error wrt theta0 where theta1 is kept fix; or vice versa.
        parabola root is expected to get closer to the middle as the algorithm proceeds.
        """
        points = deserialize_points(self.points_x, self.points_y)
        num_datapoints = 15
        step = 0.5

        if index == 0:  # fix theta1 for theta0
            x = [self.theta0 - step * (num_datapoints / 2 - i) for i in range(num_datapoints)]
            y = [j(theta0, self.theta1, points) for theta0 in x]
        else:           # fix theta0 for theta1
            x = [self.theta1 - step * (num_datapoints / 2 - i) for i in range(num_datapoints)]
            y = [j(self.theta0, theta1, points) for theta1 in x]

        plt.plot(x, y, '--bo')
        plt.title('error with respect to theta%s' % index)

        return fig_to_uri()

    def deserialized_points(self):
        return deserialize_points(self.points_x, self.points_y)

    def __str__(self):
        return 'GD(%s,%s)' % (self.theta0, self.theta1)


def h(theta0, theta1, x):
    """prediction of y values using x values with the given theta parameters"""
    return theta0 + theta1 * x


def j(theta0, theta1, points):
    """error function J(theta0, theta1) = 1/(2m) * (sum of squared errors of h_theta(x))"""
    sse = 0.0
    for point in points:
        prediction = h(theta0, theta1, point.x)
        sse += (prediction - point.y) ** 2
    return sse / 2 / len(points)


def delta_j(theta0, theta1, points, index):
    """
    find the partial derivatives of J(theta0, theta1):
    PD of J wrt theta0 = 1/m * (sum of errors of h_theta(x)),
    PD of J wrt theta1 = 1/m * (sum of (errors of h_theta(x) * xi)).
    """
    delta = 0.0
    for point in points:
        prediction = h(theta0, theta1, point.x)
        if index == 0:
            delta += (prediction - point.y)
        else:  # index == 1
            delta += (prediction - point.y) * point.x
    return delta / len(points)


def serialize_points(points):
    points_x = str(points[0].x)
    points_y = str(points[0].y)
    for point in points[1:]:
        points_x += (',' + str(point.x))
        points_y += (',' + str(point.y))
    return points_x, points_y


def deserialize_points(points_x, points_y):
    points = []
    x = [float(val) for val in points_x.split(',')]
    y = [float(val) for val in points_y.split(',')]
    for i in range(len(x)):
        points.append(Point(x[i], y[i]))
    return points


def fig_to_uri():
    """convert graph into string buffer and then we convert 64 bit code into image"""
    # this code fragment is taken from mdhvkothari
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.clf()  # clean previous graphs
    return uri


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '(%d,%d)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
