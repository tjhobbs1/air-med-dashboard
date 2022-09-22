import tablib
from import_export import resources
from .models import Flight


class FlightResource(resources.ModelResource):
    class Meta:
        model = Flight
