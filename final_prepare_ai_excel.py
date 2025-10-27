import pandas as pd
import re

# Input/Output file paths
input_file = r"C:\Users\hp\Documents\ai_questions_extracted.xlsx"


output_file = "ai_questions_final_ready.xlsx"

# Load Excel
df = pd.read_excel(input_file)

def fix_spacing(text):
    if pd.isna(text):
        return ""
    text = str(text)
    # Add spaces between letters/numbers, and units
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    text = text.replace("m/s", " m/s ").replace("kg", " kg ").replace("J", " J ").replace("N", " N ")
    text = text.replace("°", "° ").replace("√", "√ ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Clean all columns
for col in df.columns:
    df[col] = df[col].apply(fix_spacing)

# Ensure proper column structure
required_cols = ["S.No", "Question", "Option A", "Option B", "Option C", "Option D", "Correct Option"]
for col in required_cols:
    if col not in df.columns:
        df[col] = ""

df["S.No"] = range(1, len(df) + 1)
df = df[required_cols]

df.to_excel(output_file, index=False)
print(f"✅ Final import-ready Excel created: {output_file}")
print(f"✅ Total questions: {len(df)}")
