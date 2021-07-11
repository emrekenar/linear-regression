from django.shortcuts import render

from .models import GradientDescent


def index(request):
    gd = GradientDescent()
    gd.init_parameters()

    return render(request, 'index.html', context={
        'gd': gd,
        'gd_id': gd.id,
        'points': gd.deserialized_points(),
        'gd_plot_uri': gd.get_gd_plot_uri(),
        'j_theta0_plot_uri': gd.get_j_theta_plot_uri(0),
        'j_theta1_plot_uri': gd.get_j_theta_plot_uri(1)
    })


def proceed(request, gd_id):
    gd = GradientDescent.objects.get(pk=int(gd_id))
    gd.proceed()

    return render(request, 'index.html', context={
        'gd': gd,
        'gd_id': gd.id,
        'points': gd.deserialized_points(),
        'gd_plot_uri': gd.get_gd_plot_uri(),
        'j_theta0_plot_uri': gd.get_j_theta_plot_uri(0),
        'j_theta1_plot_uri': gd.get_j_theta_plot_uri(1)
    })


def run(request, gd_id):
    gd = GradientDescent.objects.get(pk=int(gd_id))
    gd.run()

    return render(request, 'index.html', context={
        'gd': gd,
        'gd_id': gd.id,
        'points': gd.deserialized_points(),
        'gd_plot_uri': gd.get_gd_plot_uri(),
        'j_theta0_plot_uri': gd.get_j_theta_plot_uri(0),
        'j_theta1_plot_uri': gd.get_j_theta_plot_uri(1)
    })
