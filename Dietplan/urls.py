from django.urls import path
from . import views


urlpatterns = [
    path('caloriescalculator/', views.caloriescalculator, name='caloriescalculator'),
    path('getdietplan/', views.getdietplan, name='get-dietplan'),
    path('ingredient/', views.ingredient, name='ingredient'),
    path('meal/', views.meal, name='meal'),
    path('vegdietplan/', views.vegdietplan, name='vegdietplan'),
    path('nonvegdietplan/', views.non_vegdietplan, name='non-vegdietplan'),
]
