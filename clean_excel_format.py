import pandas as pd
import re

# Input Excel (original messy one)
input_file = "wpe_collision_questions.xlsx"
output_file = "wpe_collision_cleaned.xlsx"

# Read all columns
df = pd.read_excel(input_file, header=None)

clean_data = []

for i, row in df.iterrows():
    # Merge all non-empty cells into one line
    line = " ".join(str(x) for x in row.tolist() if str(x) != "nan").strip()

    # Skip header lines
    if "Subject" in line or "Kishor" in line or "Physics - Section" in line:
        continue

    # Clean weird joins
    line = re.sub(r'([a-z])([A-Z])', r'\1 \2', line)
    line = re.sub(r'(\d)([A-Za-z])', r'\1 \2', line)
    line = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', line)
    line = re.sub(r'\s+', ' ', line)

    # Try to split question and options
    opts = re.findall(r'([A-D])\.\s*([^A-D]+?)(?=\s[A-D]\.|$)', line)
    options = {o[0]: o[1].strip() for o in opts}

    # Question part = text before first option
    parts = re.split(r'\s?[A-D]\.\s?', line)
    question_text = parts[0].strip()

    clean_data.append({
        "S.No": i + 1,
        "Question": question_text,
        "Option A": options.get("A", row[1] if len(row) > 1 else ""),
        "Option B": options.get("B", row[2] if len(row) > 2 else ""),
        "Option C": options.get("C", row[3] if len(row) > 3 else ""),
        "Option D": options.get("D", row[4] if len(row) > 4 else ""),
        "Correct Option": "",
    })

# Save the cleaned Excel
pd.DataFrame(clean_data).to_excel(output_file, index=False)
print(f"✅ Cleaned Excel saved successfully as: {output_file}")
