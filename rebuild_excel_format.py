import pandas as pd
import re

# Input/output files
input_file = "wpe_collision_final_cleaned.xlsx"
output_file = "wpe_collision_ready_for_import.xlsx"

# Read Excel
df = pd.read_excel(input_file)

# Step 1: Drop garbage rows
df = df[~df["Question"].astype(str).str.contains("Subject|Kishor|Standard|Date|Physics - Section", case=False, na=False)]
df = df[df["Question"].notna()]

# Step 2: Smart text cleaner
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).strip()
    # Fix missing spaces between words, numbers, and units
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', text)
    text = text.replace("m/s", " m/s").replace("kg", " kg").replace("N", " N").replace("J", " J")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Step 3: Apply cleaner
for col in ["Question", "Option A", "Option B", "Option C", "Option D"]:
    if col in df.columns:
        df[col] = df[col].apply(clean_text)

# Step 4: Fix shifted columns (if header row present)
if "Question" in df.iloc[0].to_list():
    df = df.iloc[1:]  # remove extra header row

# Step 5: Re-number serials
df["S.No"] = range(1, len(df) + 1)

# Step 6: Ensure all required columns
for col in ["Option A", "Option B", "Option C", "Option D", "Correct Option"]:
    if col not in df.columns:
        df[col] = ""

# Step 7: Final save
df = df[["S.No", "Question", "Option A", "Option B", "Option C", "Option D", "Correct Option"]]
df.to_excel(output_file, index=False)

print(f"✅ Clean formatted Excel created: {output_file}")
print(f"✅ Total questions ready: {len(df)}")
