import pdfplumber
import pandas as pd
import re
import os

pdf_path = "WPE_and_collision_948838_1_1760516000.pdf"
excel_path = "wpe_collision_questions.xlsx"

if not os.path.exists(pdf_path):
    print(f"❌ PDF not found at: {os.path.abspath(pdf_path)}")
    exit()

print(f"📄 Reading PDF: {pdf_path}")

# Step 1: Extract text from PDF
text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        page_text = page.extract_text()
        if page_text:
            # Preserve line breaks for question separation
            text += "\n" + page_text + "\n"
            print(f"✅ Extracted Page {page_num}")
        else:
            print(f"⚠️ Page {page_num} is blank or not readable")

# Step 2: Normalize and clean text
text = text.replace("\u2022", "").replace("•", "")
text = re.sub(r'\s+', ' ', text)
text = re.sub(r'(\d+)\s*\)', r'\n(\1)', text)   # ensure each question starts on a new line
text = re.sub(r'([A-D])\)', r'\n(\1)', text)    # ensure options start on new lines

# Step 3: Split into question & answer sections
match = re.search(r'Answer\s*Key', text, re.IGNORECASE)
if match:
    ans_index = match.start()
    question_section = text[:ans_index]
    answer_section = text[ans_index:]
else:
    print("⚠️ Answer key not found normally; extracting all questions")
    question_section = text
    answer_section = ""

# Step 4: Split questions more robustly
# Matches "(1)" or "1." or "Q1" etc.
question_blocks = re.split(r'\(?\b\d{1,2}\)?\s*(?=[A-Z])', question_section)
question_blocks = [q.strip() for q in question_blocks if len(q.strip()) > 20]  # remove tiny fragments

print(f"✅ Found {len(question_blocks)} questions.")
answers = re.findall(r'\d+\s*-\s*([A-D])', answer_section)
print(f"✅ Found {len(answers)} answers.")

# Step 5: Extract question text + options
data = []
for i, block in enumerate(question_blocks):
    # Extract options
    opts = re.findall(r'\(([A-D])\)\s*([^()]+)', block)
    options = {opt[0]: opt[1].strip() for opt in opts}
    q_text = re.split(r'\([A-D]\)', block)[0].strip()

    data.append({
        "S.No": i + 1,
        "Question": q_text,
        "Option A": options.get("A", ""),
        "Option B": options.get("B", ""),
        "Option C": options.get("C", ""),
        "Option D": options.get("D", ""),
        "Correct Option": answers[i] if i < len(answers) else "",
    })

# Step 6: Export Excel
df = pd.DataFrame(data)
df.to_excel(excel_path, index=False)
print(f"\n✅ Excel created successfully with {len(df)} questions.")
print(os.path.abspath(excel_path))
