from django import forms
from django import forms
from models import Airmedflights


class AirmedflightsForm(forms.ModelForm):
    class Meta:
        model = Airmedflights
        fields = {'base', 'flight_num'}
