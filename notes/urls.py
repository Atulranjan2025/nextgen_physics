from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('notes/', views.notes, name='notes'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('test/', views.test, name='test'),                
    path('submit_test/', views.submit_test, name='submit_test'),
    path('contact/', views.contact, name='contact'),
    path('simulations/', views.simulations_menu, name='simulations_menu'),
    path('simulation/<slug:slug>/', views.simulation_detail, name='simulation_detail'),


 
]
