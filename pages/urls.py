from django.urls import path
from pages import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getweather/', views.getweather, name='getweather'),
]
