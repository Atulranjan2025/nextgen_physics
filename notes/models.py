from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


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



from django.db import models

class PhysicsTest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(PhysicsTest, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ])

    def __str__(self):
        return self.question_text[:100]
class TestSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    test = models.ForeignKey(PhysicsTest, on_delete=models.CASCADE)
    current_question = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    time_spent = models.IntegerField(default=0)  # seconds
    responses = models.JSONField(default=dict)
    completed = models.BooleanField(default=False)

class TestResult(models.Model):
    session = models.OneToOneField(TestSession, on_delete=models.CASCADE)
    score = models.FloatField()
    accuracy = models.FloatField()
    details = models.JSONField()  # {q_id: {"selected": "B", "correct": "C", "time": 12}}


    
