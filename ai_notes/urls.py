from django.urls import path
from . import views

urlpatterns = [
    path('ai-notes/', views.ai_notes_view, name='ai_notes'),
]
