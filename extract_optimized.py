#!/usr/bin/env python3
"""
Optimized PDF Text Extraction Script for Image-based PDFs
Uses multiple OCR methods to extract text
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import time

# Method 1: PyMuPDF + Tesseract (High quality, good for most cases)
def extract_with_pymupdf_tesseract(pdf_path):
    """Extract text using PyMuPDF to get images, then Tesseract OCR"""
    print("\n" + "="*80)
    print("METHOD 1: PyMuPDF + Tesseract OCR")
    print("="*80)
    try:
        import fitz  # PyMuPDF
        import pytesseract
        from PIL import Image

        doc = fitz.open(pdf_path)
        full_text = []
        total_pages = len(doc)

        print(f"Total pages: {total_pages}")
        start_time = time.time()

        for page_num in range(total_pages):
            print(f"Processing page {page_num + 1}/{total_pages}...", end=' ')

            page = doc[page_num]

            # Convert page to high-resolution image (300 DPI)
            zoom = 300 / 72  # 300 DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Perform OCR with custom config for better accuracy
            custom_config = r'--oem 3 --psm 6'
            page_text = pytesseract.image_to_string(img, lang='eng', config=custom_config)

            full_text.append(f"\n{'='*80}\nPAGE {page_num + 1}\n{'='*80}\n{page_text}")
            print(f"✓ ({len(page_text)} chars)")

        doc.close()

        result = "\n".join(full_text)
        elapsed = time.time() - start_time
        print(f"\n✓ Completed in {elapsed:.1f}s")
        print(f"✓ Total characters extracted: {len(result):,}")
        return result
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


# Method 2: pdf2image + Tesseract (Alternative method)
def extract_with_pdf2image_tesseract(pdf_path):
    """Extract text using pdf2image to convert pages, then Tesseract OCR"""
    print("\n" + "="*80)
    print("METHOD 2: pdf2image + Tesseract OCR")
    print("="*80)
    try:
        from pdf2image import convert_from_path
        import pytesseract

        print("Converting PDF to images (this may take a moment)...")
        start_time = time.time()

        # Convert with high DPI for better OCR
        images = convert_from_path(pdf_path, dpi=300)
        total_pages = len(images)
        print(f"Total pages: {total_pages}")

        full_text = []
        for i, image in enumerate(images):
            print(f"Processing page {i + 1}/{total_pages}...", end=' ')

            # OCR with custom config
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='eng', config=custom_config)

            full_text.append(f"\n{'='*80}\nPAGE {i + 1}\n{'='*80}\n{text}")
            print(f"✓ ({len(text)} chars)")

        result = "\n".join(full_text)
        elapsed = time.time() - start_time
        print(f"\n✓ Completed in {elapsed:.1f}s")
        print(f"✓ Total characters extracted: {len(result):,}")
        return result
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


# Method 3: pdfplumber (Quick check for text-based PDFs)
def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber (fast for text-based PDFs)"""
    print("\n" + "="*80)
    print("METHOD 3: pdfplumber (text extraction)")
    print("="*80)
    try:
        import pdfplumber

        full_text = []
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"Total pages: {total_pages}")

            for i, page in enumerate(pdf.pages):
                print(f"Processing page {i + 1}/{total_pages}...", end=' ')
                text = page.extract_text()
                if text:
                    full_text.append(f"\n{'='*80}\nPAGE {i + 1}\n{'='*80}\n{text}")
                    print(f"✓ ({len(text)} chars)")
                else:
                    print("✗ (no text)")

        result = "\n".join(full_text)
        print(f"\n✓ Total characters extracted: {len(result):,}")
        return result if result.strip() else None
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None


def save_result(text, method_name, pdf_name):
    """Save extraction result to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("extracted_text")
    output_dir.mkdir(exist_ok=True)

    # Save with method name
    output_file = output_dir / f"{pdf_name}_{method_name}_{timestamp}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"\n📄 Saved to: {output_file}")
    print(f"📊 File size: {output_file.stat().st_size / 1024:.1f} KB")
    return output_file


def main():
    print("\n" + "="*80)
    print("PDF TEXT EXTRACTION TOOL")
    print("="*80)

    # Find PDF file
    pdf_files = list(Path(".").glob("*.pdf"))
    if not pdf_files:
        print("\n✗ No PDF files found in current directory!")
        sys.exit(1)

    pdf_path = pdf_files[0]
    print(f"\n📄 PDF File: {pdf_path}")
    print(f"📊 File size: {pdf_path.stat().st_size / (1024*1024):.2f} MB")

    pdf_name = pdf_path.stem.replace(' ', '_')

    # Try methods in order of preference
    results = {}

    # Try Method 1: PyMuPDF + Tesseract (usually best for scanned PDFs)
    print("\n" + "▶"*40)
    result1 = extract_with_pymupdf_tesseract(str(pdf_path))
    if result1:
        results['pymupdf_tesseract'] = result1
        save_result(result1, 'pymupdf_tesseract', pdf_name)

    # Try Method 2: pdf2image + Tesseract (alternative)
    print("\n" + "▶"*40)
    result2 = extract_with_pdf2image_tesseract(str(pdf_path))
    if result2:
        results['pdf2image_tesseract'] = result2
        save_result(result2, 'pdf2image_tesseract', pdf_name)

    # Try Method 3: pdfplumber (quick check)
    print("\n" + "▶"*40)
    result3 = extract_with_pdfplumber(str(pdf_path))
    if result3:
        results['pdfplumber'] = result3
        save_result(result3, 'pdfplumber', pdf_name)

    # Summary
    print("\n" + "="*80)
    print("EXTRACTION SUMMARY")
    print("="*80)

    if not results:
        print("✗ All extraction methods failed!")
        sys.exit(1)

    # Find best result (longest text)
    best_method, best_text = max(results.items(), key=lambda x: len(x[1]))

    for method, text in results.items():
        status = f"✓ {len(text):,} characters"
        marker = " ⭐ BEST" if method == best_method else ""
        print(f"{method:30s}: {status}{marker}")

    # Save best result
    best_file = save_result(best_text, 'BEST', pdf_name)

    print("\n" + "="*80)
    print("✅ EXTRACTION COMPLETE!")
    print("="*80)
    print(f"\n📁 All extracted text saved in: ./extracted_text/")
    print(f"🌟 Best result: {best_file.name}")
    print(f"📊 Total characters: {len(best_text):,}")
    print(f"📄 Estimated words: ~{len(best_text.split()):,}")


if __name__ == "__main__":
    main()
