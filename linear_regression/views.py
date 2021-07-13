from django.shortcuts import render

from .models import GradientDescent
from .forms import NumPointsForm, PointsForm


def index(request):
    gd = GradientDescent()
    gd.init_parameters()

    return render_everything(request, gd, NumPointsForm(), PointsForm(gd))


def change_num_points(request, gd_id):
    gd = GradientDescent.objects.get(pk=int(gd_id))

    if request.method == 'POST':
        form = NumPointsForm(request.POST)
        if form.is_valid():
            gd.set_num_points(int(form.data['num_points']))
        else:
            form = NumPointsForm()
            print('invalid input for num points')
    else:
        form = NumPointsForm()

    return render_everything(request, gd, form, PointsForm(gd))


def change_points(request, gd_id):
    gd = GradientDescent.objects.get(pk=int(gd_id))

    if request.method == 'POST':
        form = PointsForm(gd, request.POST)
        if form.is_valid():
            points_x = (str(form.data['x1']))
            points_y = (str(form.data['y1']))
            for i in range(1, gd.num_points):
                points_x += (',' + str(form.data['x' + str(i + 1)]))
                points_y += (',' + str(form.data['y' + str(i + 1)]))
            gd.set_points(points_x, points_y)
        else:
            form = PointsForm(gd)
            print('points are given invalid inputs')
    else:
        form = PointsForm(gd)

    return render_everything(request, gd, NumPointsForm(), form)


def proceed(request, gd_id):
    gd = GradientDescent.objects.get(pk=int(gd_id))
    gd.proceed()

    return render_everything(request, gd)


def run(request, gd_id):
    gd = GradientDescent.objects.get(pk=int(gd_id))
    gd.run()

    return render_everything(request, gd)


def render_everything(request, gd, num_points_form=None, points_form=None):
    return render(request, 'index.html', context={
        'gd': gd,
        'gd_id': gd.id,
        'num_points_form': num_points_form,
        'points_form': points_form,
        'enum_points': enumerate(gd.deserialized_points(), start=1),
        'gd_plot_uri': gd.get_gd_plot_uri(),
        'j_theta0_plot_uri': gd.get_j_theta_plot_uri(0),
        'j_theta1_plot_uri': gd.get_j_theta_plot_uri(1)
    })
