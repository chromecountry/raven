#!/usr/bin/env python3

"""
PDF parser for extracting receipt data from PDF files
"""

import re
from pathlib import Path
from typing import Dict, Optional
import pdfplumber


class ReceiptParser:
    def __init__(self) -> None:
        self.amount_pattern = r'\$?\d+\.\d{2}'
        self.date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'

    def extract_text(self, pdf_path: Path) -> str:
        """Extract text from PDF using pdfplumber"""
        text = ''
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ''
        except Exception:
            # Fallback to OCR if text extraction fails
            text = self._ocr_extract(pdf_path)
        return text

    def _ocr_extract(self, pdf_path: Path) -> str:
        """Extract text using OCR"""
        # Convert PDF to image and use OCR
        # This is a simplified version - you might need more sophisticated PDF to image conversion
        return ''

    def parse_receipt(self, pdf_path: Path) -> Dict[str, Optional[str]]:
        """Parse receipt and extract key information"""
        text = self.extract_text(pdf_path)
        
        # Extract amount
        amounts = re.findall(self.amount_pattern, text)
        amount = amounts[-1] if amounts else None
        
        # Extract date
        dates = re.findall(self.date_pattern, text)
        date = dates[0] if dates else None
        
        # Extract merchant
        merchant = self._extract_merchant(text)
        
        return {
            'amount': amount,
            'date': date,
            'merchant': merchant,
            'filename': pdf_path.name
        }

    def _extract_merchant(self, text: str) -> Optional[str]:
        """Extract merchant name from text"""
        # Common merchant patterns
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line) > 3 and not re.search(r'\d', line):
                return line
        return None 