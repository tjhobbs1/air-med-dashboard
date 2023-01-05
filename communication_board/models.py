from django.db import models


class Communication_Board(models.Model):
    date_opened = models.DateField()
    base = models.CharField(max_length=250, default='')
    issue_category = models.CharField(max_length=250, default='')
    transport_related = models.CharField(max_length=100, default='')
    reported_issue = models.TextField(max_length=1500, default='')
    reported_by_person1 = models.CharField(max_length=100, default='')
    reported_by_person2 = models.CharField(max_length=100, default='')
    issue_status = models.CharField(max_length=100, default='')
    follow_up_information = models.TextField(max_length=1500, default='')
    assigned_to_person1 = models.CharField(max_length=100, default='')
    assigned_to_person2 = models.CharField(max_length=100, default='')
    updated = models.DateTimeField(auto_now=True)
    date_closed = models.DateField(blank=True, null=True)
