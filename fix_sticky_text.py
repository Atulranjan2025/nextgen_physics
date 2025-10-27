import pandas as pd
import re

# Input/output file paths
input_file = "wpe_collision_ready_for_import.xlsx"
output_file = "wpe_collision_final_readable.xlsx"

# Read Excel
df = pd.read_excel(input_file)

# Smart Physics Auto-Spacer Function
def smart_space(text):
    if pd.isna(text):
        return ""
    text = str(text)

    # Fix letter-number and number-letter joins
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)

    # Fix lowercase-uppercase joins
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Fix units
    units = ["m/s", "m s", "m/sec", "J", "N", "kg", "cm", "mm", "g", "Hz", "W", "°", "rad", "s"]
    for u in units:
        text = text.replace(u, " " + u + " ")

    # Fix formula tokens
    text = re.sub(r'([A-Za-z])([+\-*/=])', r'\1 \2', text)
    text = re.sub(r'([+\-*/=])([A-Za-z])', r'\1 \2', text)

    # Add spacing around roots and symbols
    text = text.replace("√", "√ ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Apply to all question/option columns
for col in ["Question", "Option A", "Option B", "Option C", "Option D"]:
    if col in df.columns:
        df[col] = df[col].apply(smart_space)

# Re-number serials and save
df["S.No"] = range(1, len(df) + 1)
df.to_excel(output_file, index=False)

print(f"✅ Fixed readable Excel created: {output_file}")
print(f"✅ Total questions processed: {len(df)}")
