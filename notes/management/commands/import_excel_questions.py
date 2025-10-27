from django.core.management.base import BaseCommand
from notes.models import PhysicsTest, Question
import pandas as pd

class Command(BaseCommand):
    help = "Import Physics questions from Excel file into selected test"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to Excel file')
        parser.add_argument('test_id', type=int, help='PhysicsTest ID to link questions')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        test_id = kwargs['test_id']

        try:
            test = PhysicsTest.objects.get(id=test_id)
        except PhysicsTest.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Test with ID {test_id} not found"))
            return

        # Load Excel file
        df = pd.read_excel(file_path)
        total = 0

        for _, row in df.iterrows():
            Question.objects.create(
                test=test,
                question_text=str(row['Question']).strip(),  # ✅ Fixed field name
                option_a=str(row['Option A']).strip(),
                option_b=str(row['Option B']).strip(),
                option_c=str(row['Option C']).strip(),
                option_d=str(row['Option D']).strip(),
                correct_option=str(row['Correct Option']).strip().upper(),
            )
            total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {total} questions into '{test.title}'"))
