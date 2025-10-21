from django.shortcuts import render, get_object_or_404, redirect
from .models import PhysicsNote, Question
from django.core.paginator import Paginator
from django.contrib import messages
from .models import ContactMessage
from .models import Simulation

# ✅ Home Page View
def home(request):
    return render(request, 'notes/home.html')

# ✅ About Page View
def about(request):
    return render(request, 'notes/about.html')
from .models import Simulation
from django.shortcuts import render, get_object_or_404

# ✅ Show all simulations
def simulations_menu(request):
    simulations = Simulation.objects.all().order_by('title')
    return render(request, 'notes/simulations_menu.html', {'simulations': simulations})

# ✅ Show one specific simulation
def simulation_detail(request, slug):
    simulation = get_object_or_404(Simulation, slug=slug)
    return render(request, 'notes/simulation_detail.html', {'simulation': simulation})



def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        # ✅ Save message to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        messages.success(request, "Your message has been sent successfully! ✅")
        return redirect("/contact/")

    return render(request, "notes/contact.html")


# ✅ Notes List Page
def notes(request):
    query = request.GET.get('q')
    if query:
        all_notes = PhysicsNote.objects.filter(
            title__icontains=query
        ) | PhysicsNote.objects.filter(
            chapter__icontains=query
        )
    else:
        all_notes = PhysicsNote.objects.all().order_by('-created_at')

    paginator = Paginator(all_notes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notes/notes.html', {
        'notes': page_obj,
        'query': query,
        'page_obj': page_obj
    })

# ✅ Note Detail Page
def note_detail(request, note_id):
    note = get_object_or_404(PhysicsNote, id=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})

# ✅ Online Test Page
def test(request):
    questions = Question.objects.all()
    return render(request, 'notes/test.html', {'questions': questions})

# ✅ Test Submission Page
def submit_test(request):
    if request.method == 'POST':
        questions = Question.objects.all()
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == question.correct_answer:
                score += 1

        percentage = (score / total) * 100 if total > 0 else 0
        return render(request, 'notes/result.html', {
            'score': score,
            'total': total,
            'percentage': percentage
        })
    else:
        return redirect('/test/')
