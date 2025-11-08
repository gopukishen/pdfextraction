# PDF Text Extraction Project

This project extracts text from image-based PDFs (scanned book pages) using OCR technology.

## Extraction Results

**PDF File:** Unit 1 Drama.pdf.pdf (14.63 MB, 24 pages)

### Successfully Extracted:
- **Method 1 (PyMuPDF + Tesseract):** 82,585 characters in 163.3 seconds
- **Method 2 (pdf2image + Tesseract):** 82,395 characters in 164.1 seconds

### Output Files:
All extracted text is saved in the `extracted_text/` directory:
- `Unit_1_Drama.pdf_pymupdf_tesseract_*.txt` - Best quality extraction
- `Unit_1_Drama.pdf_pdf2image_tesseract_*.txt` - Alternative extraction

## Usage

### Quick Extraction:
```bash
python3 extract_optimized.py
```

This will automatically:
1. Find all PDF files in the current directory
2. Extract text using multiple OCR methods
3. Save results to `extracted_text/` folder
4. Create a comparison of all methods

### Requirements:
System packages:
- tesseract-ocr
- poppler-utils

Python packages:
- PyMuPDF (fitz)
- pytesseract
- pdf2image
- Pillow
- numpy
- opencv-python

Install with:
```bash
./install_ocr.sh
pip install -r requirements.txt
```

## Methods Used

1. **PyMuPDF + Tesseract OCR** - Converts PDF pages to images at 300 DPI, then performs OCR
2. **pdf2image + Tesseract OCR** - Alternative conversion method
3. **pdfplumber** - Quick text extraction (for text-based PDFs)

## Content

The extracted PDF contains educational material about drama and literature, including:
- Questions about Elizabethan dramatists (Marlowe, Kyd, Shakespeare)
- Literary analysis questions
- Aristotelian dramatic theory
- UGC NET examination questions

## Notes

- OCR accuracy depends on image quality
- Some special characters may not be recognized perfectly
- Processing time: ~3 minutes per page at 300 DPI
