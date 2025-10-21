from django.db import models
from django.utils.text import slugify

class PhysicsNote(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.CharField(max_length=50, default="Physics")
    chapter = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='notes_pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Simulation(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='simulation_thumbnails/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    content_html = models.TextField(blank=True, help_text="Optional custom HTML/JS simulation code")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Simulation, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class Question(models.Model):
    chapter = models.CharField(max_length=100)
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')]
    )

    def __str__(self):
        return f"{self.chapter}: {self.question_text[:50]}"


    
