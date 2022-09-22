from django.db import models

# Create your models here.


class Flight(models.Model):
    transport_date = models.DateField()
    flight_num = models.CharField(
        primary_key=True, unique=True, max_length=100, default='')
    base = models.CharField(max_length=100)

    class Meta:
        db_table = "flight"
