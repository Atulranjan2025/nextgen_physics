from django.shortcuts import render
from django.conf import settings
import os
import markdown
import requests
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
from google import genai
import matplotlib
matplotlib.use('Agg')  # Prevents GUI-related crash on Windows


# ✅ Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def ai_notes_view(request):
    topic = request.GET.get("topic")
    notes_html = None
    error = None
    pdf_path = None

    if topic:
        try:
            # 1️⃣ Generate Physics Notes using Gemini
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=f"""
                You are an expert NEET/JEE Physics teacher.
                Create detailed, structured notes on "{topic}" including:
                - Summary
                - Key Formulas (use LaTeX)
                - Graphical Interpretation
                - Conceptual Explanation
                - NEET/JEE-level Examples
                Output should be in Markdown format.
                """
            )
            notes_text = response.text
            notes_html = markdown.markdown(notes_text)

            # Create media folder
            media_path = os.path.join(settings.BASE_DIR, "media")
            os.makedirs(media_path, exist_ok=True)

            # 2️⃣ Smart AI Diagram Generator (based on topic)
            diagram_prompt = generate_diagram_prompt(topic)
            concept_path = os.path.join(media_path, f"{topic}.png")

            try:
                diagram_img = client.images.generate(
                    model="models/imagen-3.0-fast-generate-001",
                    prompt=diagram_prompt
                )
                diagram_url = diagram_img.data[0].url
                response = requests.get(diagram_url, timeout=15)
                response.raise_for_status()
                with open(concept_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Diagram generated for: {topic}")
            except Exception as e:
                print("⚠️ Gemini diagram failed:", e)
                draw_default_diagram(topic, concept_path)

            # 3️⃣ Smart Graph Generator
            graph_prompt = generate_graph_prompt(topic)
            graph_path = os.path.join(media_path, f"{topic}_graph.png")

            try:
                graph_img = client.images.generate(
                    model="models/imagen-3.0-fast-generate-001",
                    prompt=graph_prompt
                )
                graph_url = graph_img.data[0].url
                response = requests.get(graph_url, timeout=15)
                response.raise_for_status()
                with open(graph_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Graph generated for: {topic}")
            except Exception as e:
                print("⚠️ Gemini graph failed:", e)
                generate_fallback_graph(topic, graph_path)

            # 4️⃣ Create PDF (Notes + Diagram + Graph)
            pdf_path = os.path.join(media_path, f"{topic}_notes.pdf")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, f"AI Physics Notes: {topic.title()}", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, txt=notes_text.replace("**", "").replace("*", ""))

            if os.path.exists(concept_path):
                pdf.add_page()
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Concept Diagram", ln=True)
                pdf.image(concept_path, x=25, w=160)

            if os.path.exists(graph_path):
                pdf.add_page()
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Graphical Interpretation", ln=True)
                pdf.image(graph_path, x=25, w=160)

            pdf.output(pdf_path)
            print(f"✅ PDF saved: {pdf_path}")

        except Exception as e:
            error = str(e)

    return render(request, "ai_notes/result.html", {
        "topic": topic,
        "notes": notes_html,
        "pdf_path": pdf_path,
        "error": error
    })


# 🧠 Auto-generate diagram prompt from topic
def generate_diagram_prompt(topic):
    mapping = {
        "work": "a block being pulled by a force F at an angle θ on a horizontal surface",
        "energy": "a ball rolling down an inclined plane showing PE and KE conversion",
        "projectile": "a projectile motion path showing velocity components and angle θ",
        "shm": "a spring-mass system oscillating about mean position",
        "circular motion": "an object in uniform circular motion with centripetal force",
        "friction": "a block on rough surface showing frictional force opposite to motion",
        "momentum": "two colliding balls showing velocities before and after collision",
        "gravitation": "Earth and satellite system showing gravitational force vectors",
    }
    return f"Draw a neat, labeled physics diagram of {mapping.get(topic.lower(), topic)}."


# 🧠 Auto-generate graph prompt from topic
def generate_graph_prompt(topic):
    mapping = {
        "work": "Force vs Displacement graph showing area representing work done",
        "energy": "Potential energy vs position graph showing U ∝ -1/r behavior",
        "projectile": "Parabolic trajectory y vs x showing motion path",
        "shm": "Displacement vs Time graph showing sinusoidal motion",
        "circular motion": "Angular velocity vs time graph for uniform motion",
        "friction": "Frictional force vs Normal reaction graph showing μN relation",
        "momentum": "Impulse vs time graph showing area equals change in momentum",
        "gravitation": "Gravitational potential vs distance graph showing inverse curve",
    }
    return f"Plot a labeled {mapping.get(topic.lower(), 'relevant physics graph for ' + topic)}."


# 🧩 Fallback if Gemini fails
def generate_fallback_graph(topic, save_path):
    x = np.linspace(0, 10, 100)
    if "work" in topic.lower():
        F = 3 * np.sqrt(x)
        title = "Force vs Displacement"
        ylabel = "Force (F)"
        xlabel = "Displacement (x)"
    elif "shm" in topic.lower():
        F = np.sin(x)
        title = "Displacement vs Time"
        ylabel = "Displacement"
        xlabel = "Time (t)"
    else:
        F = np.sin(x)
        title = f"{topic.title()} Graph"
        ylabel = "Quantity"
        xlabel = "Parameter"

    plt.figure(figsize=(5, 4))
    plt.plot(x, F, color='blue', linewidth=2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()
    print(f"✅ Offline graph created for {topic}")


# 🧩 Default Diagram Drawer (when Gemini fails)
def draw_default_diagram(topic, save_path):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')

    # Draw base
    ax.plot([0, 10], [1, 1], color='black', lw=2)
    rect = plt.Rectangle((4, 1), 1.5, 1.5, fc='lightgray', ec='black', lw=2)
    ax.add_patch(rect)
    ax.arrow(5.75, 1.75, 2, 0, head_width=0.2, head_length=0.3, fc='red', ec='red', lw=2)
    ax.text(8, 1.8, 'F', fontsize=14, color='red')
    ax.arrow(5.0, 0.5, 2, 0, head_width=0.15, head_length=0.3, fc='blue', ec='blue', lw=2)
    ax.text(7.2, 0.3, 'Displacement (x)', fontsize=12, color='blue')
    ax.text(6, 2.5, r'θ', fontsize=14, color='purple')
    ax.axis('off')
    plt.title(f'{topic.title()} Diagram (Offline)', fontsize=14)
    plt.savefig(save_path)
    plt.close()
    print(f"✅ Offline concept diagram for {topic}")
