from django.contrib import admin
from .models import PhysicsNote
from .models import Question
from .models import ContactMessage
from .models import Simulation

@admin.register(PhysicsNote)
class PhysicsNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'subject', 'created_at')
    search_fields = ('title', 'chapter')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'question_text', 'correct_answer')
    search_fields = ('chapter', 'question_text')
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

