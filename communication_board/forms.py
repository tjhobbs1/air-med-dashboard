from django import forms
from django.contrib.admin.widgets import AdminDateWidget

BASE_CHOICES = (
    ('', 'Select A Base'),
    ('Des Moines', 'Des Moines'),
    ('Knoxville', 'Knoxville'),
    ('NA', 'NA')
)

ISSUE_CHOICE = (
    ('', 'Select A Issue'),
    ('Safety', 'Safety'),
    ('Maintenance', 'Maintenance'),
    ('Equipment', 'Equipment'),
    ('Communication', 'Communication')
)

STATUS_CHOICE = (
    ('', 'Select A Status'),
    ('Open', 'Open'),
    ('Closed', 'Closed'),
    ('Under Investigation', 'Under Investigation')
)

ASSIGNED_CHOICE = (
    ('', 'Assigned To'),
    ('Leadership', 'Leadership'),
    ('AirMethods', 'Air Methods'),
    ('Communication', 'Communication'),
    ('NA', 'N/A')
)


class DateInput(forms.DateInput):
    input_type = 'date'


class CommunicationAdminForm(forms.Form):
    date_opened = forms.DateField(input_formats=['%Y-%m-%d'], widget=DateInput)
    base = forms.CharField(required=False,
                           label='Base:', widget=forms.Select(choices=BASE_CHOICES))
    issue_category = forms.CharField(required=False,
                                     label='Base:', widget=forms.Select(choices=ISSUE_CHOICE))
    transport_related = forms.CharField(required=False,
                                        label='Transport Related?', widget=forms.Select(choices=(('yes', 'Yes'), ('no', 'No'))))
    reported_issue = forms.CharField(required=False, label='Reported Issue',
                                     widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}))
    reported_by_person1 = forms.CharField(
        required=False, label='Reporting Person 1')
    reported_by_person2 = forms.CharField(
        required=False, label='Reporting Person 2')
    issue_status = forms.CharField(required=False,
                                   label='Status:', widget=forms.Select(choices=STATUS_CHOICE))
    follow_up_information = forms.CharField(required=False, label='Follow up Information',
                                            widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}))
    assigned_to_person1 = forms.CharField(required=False,
                                          label='Assigned to Person 1:', widget=forms.Select(choices=ASSIGNED_CHOICE))
    assigned_to_person2 = forms.CharField(required=False,
                                          label='Assigned to Person 2:', widget=forms.Select(choices=ASSIGNED_CHOICE))
    date_closed = forms.DateField(required=False, input_formats=[
                                  '%Y-%m-%d'], widget=DateInput)
