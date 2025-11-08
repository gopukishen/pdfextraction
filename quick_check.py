#!/usr/bin/env python3
"""Quick check to see if PDF has extractable text or needs OCR"""

import fitz  # PyMuPDF
from pathlib import Path

pdf_files = list(Path(".").glob("*.pdf"))
if not pdf_files:
    print("No PDF found")
    exit(1)

pdf_path = pdf_files[0]
print(f"Checking: {pdf_path}")

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

total_text_length = 0
for page_num in range(min(3, len(doc))):  # Check first 3 pages
    page = doc[page_num]
    text = page.get_text()
    total_text_length += len(text.strip())
    print(f"Page {page_num + 1}: {len(text.strip())} chars")

doc.close()

if total_text_length < 100:
    print("\n⚠ PDF appears to be image-based - OCR required!")
else:
    print("\n✓ PDF has extractable text")
