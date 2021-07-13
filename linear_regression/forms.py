from django import forms


class NumPointsForm(forms.Form):
    num_points = forms.IntegerField(label='Number of points', min_value=2, max_value=99, initial=10)


class PointsForm(forms.Form):
    def __init__(self, gd=None, *args, **kwargs):
        super(PointsForm, self).__init__(*args, **kwargs)
        current_points = gd.deserialized_points()
        num = gd.num_points
        for i in range(num):
            self.fields['x' + str(i + 1)] = forms.FloatField(min_value=-999, max_value=999, initial=current_points[i].x)
            self.fields['y' + str(i + 1)] = forms.FloatField(min_value=-999, max_value=999, initial=current_points[i].y)
