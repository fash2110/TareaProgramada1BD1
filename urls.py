from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('sistema/', views.sistema, name='sistema'),
    path('sistema/insertar/', views.insertar, name='insertar'),
    path('thanks/', views.thanks, name='thanks'),
]