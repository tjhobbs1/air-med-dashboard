from dataclasses import field
from random import choices
from tkinter import Widget
import django_filters
from django import forms
from models import Airmedflights


class AirmedflightsFilter(django_filters.FilterSet):
    flight_num = django_filters.CharFilter(
        field_name='flight_num', lookup_expr='iexact')
    transport_date = django_filters.DateFromToRangeFilter(
        field_name='transport_date', lookup_expr='')
    call_type = django_filters.AllValuesMultipleFilter(
        field_name='call_type')
    outcome = django_filters.AllValuesMultipleFilter(
        field_name='outcome')

    class Meta:
        model = Airmedflights
        fields = {
            'base': ['exact'],
            'call_type': ['exact']
        }


class AirMedDashboardFilter(django_filters.FilterSet):
    transport_date = django_filters.DateFromToRangeFilter(
        field_name='transport_date', widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd'}))
    call_type = django_filters.AllValuesMultipleFilter(
        field_name='call_type', widget=forms.CheckboxSelectMultiple)
