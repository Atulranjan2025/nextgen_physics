from django.contrib import admin
from .models import PhysicsNote, ContactMessage, Simulation, PhysicsTest, Question

@admin.register(PhysicsNote)
class PhysicsNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'subject', 'created_at')
    search_fields = ('title', 'chapter')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(PhysicsTest)
class PhysicsTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_created')
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'test', 'correct_option')  # ✅ Fixed fields
    search_fields = ('question_text',)
    list_filter = ('test',)
@admin.action(description="Import questions from JSON")
def import_from_json(modeladmin, request, queryset):
    for test in queryset:
        import_questions_from_json(test)

