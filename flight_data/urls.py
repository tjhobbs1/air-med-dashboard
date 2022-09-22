from django.urls import path, include
from . import views


urlpatterns = [
    path('upload_csv/', views.upload_csv, name="upload_csv"),
    path('success/', views.upload_success, name="upload_success"),
    path('flight_data/', views.flight_data, name="flight_data"),
    path('search/', views.flight_search, name="search"),
]
