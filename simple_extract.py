#!/usr/bin/env python3
"""
Simple PDF to Text Extractor
Quick script for extracting text from image-based PDFs
"""

import sys
from pathlib import Path

def extract_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF + Tesseract"""
    import fitz
    import pytesseract
    from PIL import Image

    doc = fitz.open(pdf_path)
    full_text = []

    for page_num in range(len(doc)):
        print(f"Processing page {page_num + 1}/{len(doc)}...")
        page = doc[page_num]

        # Convert to image at 300 DPI
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # OCR
        text = pytesseract.image_to_string(img, lang='eng')
        full_text.append(f"\n--- Page {page_num + 1} ---\n{text}")

    doc.close()
    return "\n".join(full_text)

if __name__ == "__main__":
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else list(Path(".").glob("*.pdf"))[0]

    print(f"Extracting: {pdf_file}")
    text = extract_pdf(pdf_file)

    # Save
    output = Path(f"{Path(pdf_file).stem}_extracted.txt")
    output.write_text(text, encoding='utf-8')

    print(f"\n✓ Saved to: {output}")
    print(f"✓ Characters: {len(text):,}")
