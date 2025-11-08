#!/usr/bin/env python3
"""
Comprehensive PDF Text Extraction Script
Uses multiple OCR methods to extract text from image-based PDFs
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Method 1: PyMuPDF + Tesseract
def extract_with_pymupdf_tesseract(pdf_path):
    """Extract text using PyMuPDF to get images, then Tesseract OCR"""
    print("\n=== Method 1: PyMuPDF + Tesseract ===")
    try:
        import fitz  # PyMuPDF
        import pytesseract
        from PIL import Image
        import io

        doc = fitz.open(pdf_path)
        full_text = []

        for page_num in range(len(doc)):
            print(f"Processing page {page_num + 1}/{len(doc)}...")
            page = doc[page_num]

            # First try to extract any existing text
            text = page.get_text()
            if text.strip():
                full_text.append(f"\n--- Page {page_num + 1} ---\n{text}")
                continue

            # If no text, perform OCR on page images
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Perform OCR
            page_text = pytesseract.image_to_string(img, lang='eng')
            full_text.append(f"\n--- Page {page_num + 1} ---\n{page_text}")

        doc.close()
        result = "\n".join(full_text)
        print(f"Extracted {len(result)} characters")
        return result
    except Exception as e:
        print(f"Error with PyMuPDF+Tesseract: {e}")
        return None


# Method 2: pdf2image + Tesseract
def extract_with_pdf2image_tesseract(pdf_path):
    """Extract text using pdf2image to convert pages, then Tesseract OCR"""
    print("\n=== Method 2: pdf2image + Tesseract ===")
    try:
        from pdf2image import convert_from_path
        import pytesseract

        # Convert PDF to images
        print("Converting PDF to images...")
        images = convert_from_path(pdf_path, dpi=300)

        full_text = []
        for i, image in enumerate(images):
            print(f"Processing page {i + 1}/{len(images)}...")
            text = pytesseract.image_to_string(image, lang='eng')
            full_text.append(f"\n--- Page {i + 1} ---\n{text}")

        result = "\n".join(full_text)
        print(f"Extracted {len(result)} characters")
        return result
    except Exception as e:
        print(f"Error with pdf2image+Tesseract: {e}")
        return None


# Method 3: EasyOCR
def extract_with_easyocr(pdf_path):
    """Extract text using EasyOCR (deep learning-based OCR)"""
    print("\n=== Method 3: EasyOCR ===")
    try:
        import easyocr
        import fitz
        from PIL import Image
        import numpy as np

        reader = easyocr.Reader(['en'])
        doc = fitz.open(pdf_path)
        full_text = []

        for page_num in range(len(doc)):
            print(f"Processing page {page_num + 1}/{len(doc)}...")
            page = doc[page_num]

            # Convert page to image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_array = np.array(img)

            # Perform OCR
            results = reader.readtext(img_array)
            page_text = "\n".join([text[1] for text in results])
            full_text.append(f"\n--- Page {page_num + 1} ---\n{page_text}")

        doc.close()
        result = "\n".join(full_text)
        print(f"Extracted {len(result)} characters")
        return result
    except Exception as e:
        print(f"Error with EasyOCR: {e}")
        return None


# Method 4: pdfplumber (for comparison, works better with text-based PDFs)
def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber"""
    print("\n=== Method 4: pdfplumber ===")
    try:
        import pdfplumber

        full_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                print(f"Processing page {i + 1}/{len(pdf.pages)}...")
                text = page.extract_text()
                if text:
                    full_text.append(f"\n--- Page {i + 1} ---\n{text}")

        result = "\n".join(full_text)
        print(f"Extracted {len(result)} characters")
        return result if result.strip() else None
    except Exception as e:
        print(f"Error with pdfplumber: {e}")
        return None


def save_results(results, pdf_name):
    """Save extraction results to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("extracted_text")
    output_dir.mkdir(exist_ok=True)

    # Save individual method results
    for method_name, text in results.items():
        if text:
            output_file = output_dir / f"{pdf_name}_{method_name}_{timestamp}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved: {output_file}")

    # Find the best result (longest text)
    best_method = max(results.items(), key=lambda x: len(x[1]) if x[1] else 0)
    if best_method[1]:
        best_output = output_dir / f"{pdf_name}_BEST_{timestamp}.txt"
        with open(best_output, 'w', encoding='utf-8') as f:
            f.write(f"Best extraction method: {best_method[0]}\n")
            f.write("=" * 80 + "\n\n")
            f.write(best_method[1])
        print(f"\n✓ Best result saved to: {best_output}")
        return best_output

    return None


def main():
    # Find PDF file
    pdf_files = list(Path(".").glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in current directory!")
        sys.exit(1)

    pdf_path = pdf_files[0]
    print(f"Processing: {pdf_path}")
    print(f"File size: {pdf_path.stat().st_size / (1024*1024):.2f} MB")

    # Try all extraction methods
    results = {}

    # Method 1: PyMuPDF + Tesseract
    results['pymupdf_tesseract'] = extract_with_pymupdf_tesseract(str(pdf_path))

    # Method 2: pdf2image + Tesseract
    results['pdf2image_tesseract'] = extract_with_pdf2image_tesseract(str(pdf_path))

    # Method 3: EasyOCR
    results['easyocr'] = extract_with_easyocr(str(pdf_path))

    # Method 4: pdfplumber (quick check)
    results['pdfplumber'] = extract_with_pdfplumber(str(pdf_path))

    # Summary
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    for method, text in results.items():
        status = f"✓ {len(text)} chars" if text else "✗ Failed"
        print(f"{method:25s}: {status}")

    # Save results
    pdf_name = pdf_path.stem
    best_file = save_results(results, pdf_name)

    if best_file:
        print(f"\n✓ Extraction complete! Check the 'extracted_text' folder.")
    else:
        print("\n✗ All extraction methods failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
