from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.board, name="board"),
    path('board_admin/', views.board_admin, name="board_admin"),
    path('success/', views.success, name="success"),

]
