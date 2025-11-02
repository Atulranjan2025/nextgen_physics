from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('notes/', views.notes, name='notes'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('contact/', views.contact, name='contact'),

    path('simulations/', views.simulations_menu, name='simulations_menu'),
    path('simulation/<slug:slug>/', views.simulation_detail, name='simulation_detail'),

    path('test/', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.start_test, name='start_test'),
    path('save_progress/', views.save_progress, name='save_progress'),
    path('submit_test/', views.submit_test, name='submit_test'),
    path('result/<int:session_id>/', views.view_result, name='view_result'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('sim/projectile/', views.sim_projectile, name='sim_projectile'),
    path('sim/oblique/', views.sim_oblique_collision, name='sim_oblique_collision'),
    path('ydse/', views.ydse_simulation, name='ydse_simulation'),

    # ✅ NEW LINE BELOW — Projectile Simulation

]
