#!/bin/bash
# Install OCR dependencies

echo "Installing Tesseract OCR..."
apt-get install -y --fix-missing tesseract-ocr tesseract-ocr-eng 2>/dev/null || {
    echo "Trying alternative method..."
    # Download and install tesseract manually if needed
}

echo "Installing poppler-utils..."
apt-get install -y --fix-missing poppler-utils 2>/dev/null

echo "Installing system libraries..."
apt-get install -y --fix-missing libgl1-mesa-glx libglib2.0-0 2>/dev/null

echo "Checking installations..."
which tesseract && tesseract --version
which pdfimages && pdfimages -v
