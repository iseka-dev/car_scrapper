from django.urls import path
from . import views

urlpatterns = [
    path('scrap/', views.scrap, name='scrap'),
    path('cars_list/', views.cars_list)
]
