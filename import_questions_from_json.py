import json
import os
from django.core.files import File
from notes.models import PhysicsTest, Question  # 👈 app name 'notes' है तो इसे वैसा ही रखो

def import_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    test_title = data.get('title')
    description = data.get('description', '')
    test, _ = PhysicsTest.objects.get_or_create(
        title=test_title, defaults={'description': description}
    )

    for q in data['questions']:
        question = Question(
            test=test,
            question_text=q['question_text'],
            option_a=q['option_a'],
            option_b=q['option_b'],
            option_c=q['option_c'],
            option_d=q['option_d'],
            correct_option=q['correct_option']
        )

        # ✅ If image exists, attach it
        if 'image' in q and q['image'] and os.path.exists(q['image']):
            with open(q['image'], 'rb') as img_file:
                question.image.save(os.path.basename(q['image']), File(img_file), save=False)

        question.save()

    print(f"✅ Imported {len(data['questions'])} questions into '{test_title}' test.")
