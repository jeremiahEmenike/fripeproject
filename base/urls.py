from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hauts/', views.hauts, name='hauts'),
    path('robes/', views.robes, name='robes'),
    path('pantalons/', views.pantalons, name='pantalon'),
    path('jupes/', views.jupes, name='jupes'),
    path('contact/', views.contact, name='contact'),
    
    
]