from django.urls import path, include
from . import views


urlpatterns = [
    path('upload_qi_csv/', views.upload_qi_csv, name="upload_qi_csv"),
    path('quality_dashboard/', views.quality_dashboard, name='quality_dashboard'),
]
