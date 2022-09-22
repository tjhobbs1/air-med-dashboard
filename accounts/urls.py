from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('team_dashboard/', views.team_dashboard, name='team_dashboard'),
    path('request_password/', views.request_password, name='request_password'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_validate/<uidb64>/<token>/',
         views.reset_password_validate, name='reset_password_validate'),
]
