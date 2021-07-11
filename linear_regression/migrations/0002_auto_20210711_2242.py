# Generated by Django 3.2.5 on 2021-07-11 19:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('linear_regression', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradientdescent',
            name='acceptable_range',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='gradientdescent',
            name='alpha',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='gradientdescent',
            name='error',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='gradientdescent',
            name='max_steps',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gradientdescent',
            name='points_x',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='gradientdescent',
            name='points_y',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='gradientdescent',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='gradientdescent',
            name='theta0',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='gradientdescent',
            name='theta1',
            field=models.FloatField(default=0.0),
        ),
    ]
