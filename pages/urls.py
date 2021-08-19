from django.urls import path

from . import views, opskrifter

urlpatterns = [
    path('', views.index, name='index'),
    path('/opskrifter', views.opskrifter, name='opskrifter'),
]