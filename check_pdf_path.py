import os

PDF_PATH = "WPE_and_collision_948838_1_1760516000.pdf"

print("📂 Full Path:", os.path.abspath(PDF_PATH))
print("✅ File Exists:", os.path.exists(PDF_PATH))

if os.path.exists(PDF_PATH):
    print("📏 File Size:", os.path.getsize(PDF_PATH), "bytes")
else:
    print("❌ File not found! Please move it to this folder.")
