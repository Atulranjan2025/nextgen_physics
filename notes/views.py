from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import json, os, pandas as pd
from django.conf import settings

from .models import (
    PhysicsNote,
    Simulation,
    ContactMessage,
    PhysicsTest,
    Question,
    TestSession,
    TestResult
)

# =====================================================
# ✅ BASIC PAGES
# =====================================================

def home(request):
    return render(request, 'notes/home.html')

def about(request):
    return render(request, 'notes/about.html')

def contact(request):
    """Contact page with message saving."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, message=message_text)
        messages.success(request, "Your message has been sent successfully! ✅")
        return redirect("/contact/")

    return render(request, "notes/contact.html")


# =====================================================
# ✅ NOTES SYSTEM
# =====================================================

def notes(request):
    """List of all physics notes with search and pagination."""
    query = request.GET.get('q')
    if query:
        all_notes = PhysicsNote.objects.filter(title__icontains=query) | PhysicsNote.objects.filter(chapter__icontains=query)
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


def note_detail(request, note_id):
    """Show single note."""
    note = get_object_or_404(PhysicsNote, id=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})


# =====================================================
# ✅ SIMULATION SYSTEM
# =====================================================

def simulations_menu(request):
    simulations = Simulation.objects.all().order_by('title')
    return render(request, 'notes/simulations_menu.html', {'simulations': simulations})

def simulation_detail(request, slug):
    simulation = get_object_or_404(Simulation, slug=slug)
    return render(request, 'notes/simulation_detail.html', {'simulation': simulation})


# =====================================================
# ✅ TEST SYSTEM
# =====================================================

def test_list(request):
    """List all available tests."""
    tests = PhysicsTest.objects.all().order_by('id')
    return render(request, 'notes/test_list.html', {'tests': tests})


def start_test(request, test_id):
    """Start or resume a test."""
    test = get_object_or_404(PhysicsTest, id=test_id)

    session, created = TestSession.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None,
        test=test,
        completed=False
    )

    questions = test.questions.all()
    return render(request, 'notes/test.html', {
        'test': test,
        'session': session,
        'questions': questions,
    })


def save_progress(request):
    """Auto-save selected options while attempting test."""
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            session_id = data.get("session_id")
            question_id = data.get("question_id")
            selected_option = data.get("selected_option")
            time_spent = data.get("time_spent", 0)

            session = get_object_or_404(TestSession, id=session_id)
            responses = session.responses or {}
            responses[str(question_id)] = selected_option
            session.responses = responses
            session.time_spent = time_spent
            session.save()

            return JsonResponse({"status": "success", "message": "Progress saved."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request."})


def submit_test(request):
    """Submit test and evaluate result."""
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body.decode('utf-8'))
                session_id = data.get("session_id")
            else:
                session_id = request.POST.get("session_id")

            if not session_id:
                return JsonResponse({"status": "error", "message": "Missing session_id"}, status=400)

            session = get_object_or_404(TestSession, id=session_id)
            test = session.test

            correct = 0
            total = test.questions.count()
            details = {}

            for q in test.questions.all():
                selected = session.responses.get(str(q.id))
                correct_option = q.correct_option
                if selected == correct_option:
                    correct += 1
                details[q.id] = {"selected": selected, "correct": correct_option}

            score = (correct / total) * 100 if total > 0 else 0
            accuracy = (correct / total) * 100 if total > 0 else 0

            TestResult.objects.create(
                session=session,
                score=score,
                accuracy=accuracy,
                details=details
            )

            session.completed = True
            session.save()

            if request.content_type == "application/json":
                return JsonResponse({
                    "status": "success",
                    "score": score,
                    "accuracy": accuracy
                })
            else:
                return redirect(f"/result/{session.id}/")

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


# =====================================================
# ✅ RESULT VIEW (DETAILED ANALYSIS)
# =====================================================

def view_result(request, session_id):
    """Display detailed result analysis with full answers."""
    session = get_object_or_404(TestSession, id=session_id)
    result = get_object_or_404(TestResult, session=session)
    test = session.test

    reviewed_questions = []
    correct = wrong = unanswered = 0

    for q in test.questions.all():
        q_id = str(q.id)
        selected = result.details.get(q_id, {}).get("selected")
        correct_opt = result.details.get(q_id, {}).get("correct")

        options = {
            "A": q.option_a,
            "B": q.option_b,
            "C": q.option_c,
            "D": q.option_d,
        }

        selected_text = options.get(selected, None)
        correct_text = options.get(correct_opt, None)

        if selected is None:
            unanswered += 1
        elif selected == correct_opt:
            correct += 1
        else:
            wrong += 1

        reviewed_questions.append({
            "question": q,
            "selected": selected,
            "selected_text": selected_text,
            "correct": correct_opt,
            "correct_text": correct_text,
            "is_correct": selected == correct_opt if selected else False
        })

    context = {
        "session": session,
        "result": result,
        "test": test,
        "correct": correct,
        "wrong": wrong,
        "unanswered": unanswered,
        "total": test.questions.count(),
        "score": result.score,
        "accuracy": result.accuracy,
        "questions": reviewed_questions,
    }
    return render(request, "notes/result.html", context)


# =====================================================
# ✅ DASHBOARD
# =====================================================

def dashboard(request):
    """Show all completed test results."""
    sessions = TestSession.objects.filter(completed=True).order_by('-start_time')
    results = TestResult.objects.filter(session__in=sessions).select_related('session__test')

    total_tests = results.count()
    avg_score = results.aggregate(Avg('score'))['score__avg'] or 0
    avg_accuracy = results.aggregate(Avg('accuracy'))['accuracy__avg'] or 0

    labels = [r.session.test.title for r in results]
    scores = [r.score for r in results]
    accuracies = [r.accuracy for r in results]

    context = {
        "results": results,
        "total_tests": total_tests,
        "avg_score": avg_score,
        "avg_accuracy": avg_accuracy,
        "labels": labels,
        "scores": scores,
        "accuracies": accuracies,
    }
    return render(request, "notes/dashboard.html", context)
