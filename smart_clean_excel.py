import pandas as pd
import re

# Input/output files
input_file = "wpe_collision_questions.xlsx"          # original messy Excel
output_file = "wpe_collision_final_cleaned.xlsx"     # final cleaned Excel

# Read Excel without header
df = pd.read_excel(input_file, header=None)

def fix_spacing(text):
    """Add spaces between physics terms, units, numbers, and words."""
    if pd.isna(text):
        return ""
    text = str(text)

    # Insert space between lowercase-uppercase, letter-number, number-letter
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)

    # Add space before units (m/s, kg, N, J, etc.)
    text = re.sub(r'(?<=\d)(?=[a-zA-Z])', ' ', text)
    text = text.replace("m/s", " m/s").replace("kg", " kg").replace("N", " N").replace("J", " J")
    text = text.replace("°", "° ").replace("√", "√ ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

clean_rows = []

for i, row in df.iterrows():
    # Merge row text (skip NaN)
    parts = [fix_spacing(x) for x in row.tolist() if str(x) != "nan"]
    if not parts:
        continue

    line = " ".join(parts)

    # Skip header lines
    if "Subject" in line or "Physics - Section" in line or "Kishor" in line:
        continue

    # Split first segment as question, remaining as options
    question = fix_spacing(parts[0])
    opts = parts[1:] + ["", "", "", ""]  # ensure 4 slots
    clean_rows.append({
        "S.No": i + 1,
        "Question": question,
        "Option A": fix_spacing(opts[0]),
        "Option B": fix_spacing(opts[1]),
        "Option C": fix_spacing(opts[2]),
        "Option D": fix_spacing(opts[3]),
        "Correct Option": ""
    })

pd.DataFrame(clean_rows).to_excel(output_file, index=False)
print(f"✅ Final cleaned Excel created: {output_file}")
print(f"✅ Total rows processed: {len(clean_rows)}")
