"""
PDF report parser for MedGuardian.

Extraction strategy (in order of preference):
  1. pdfplumber — direct text extraction (works for text-based PDFs).
  2. PyMuPDF + pytesseract — renders each page to an image and runs OCR
     (fallback for scanned / image-only PDFs).

After text extraction, ``parse_biomarkers`` searches the raw text for
common lab-report patterns using regular expressions and returns a
dictionary of float values keyed by biomarker name.
"""

from __future__ import annotations

import io
import logging
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Return the raw text content of a PDF supplied as bytes.

    Tries pdfplumber first; falls back to PyMuPDF + Tesseract OCR if the
    direct extraction yields no usable text.

    Args:
        pdf_bytes: Raw bytes of the uploaded PDF file.

    Returns:
        A single string containing all extracted text, or an empty string
        if extraction fails entirely.
    """
    text = _extract_with_pdfplumber(pdf_bytes)
    if text.strip():
        logger.info("Text extracted via pdfplumber (%d chars).", len(text))
        return text

    logger.warning("pdfplumber returned empty text; attempting OCR fallback.")
    text = _extract_with_ocr(pdf_bytes)
    if text.strip():
        logger.info("Text extracted via OCR (%d chars).", len(text))
    else:
        logger.error("Both extraction methods returned empty text.")
    return text


def _extract_with_pdfplumber(pdf_bytes: bytes) -> str:
    try:
        import pdfplumber  # type: ignore

        pages: list[str] = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                pages.append(page_text)
        return "\n".join(pages)
    except Exception as exc:
        logger.warning("pdfplumber extraction failed: %s", exc)
        return ""


def _extract_with_ocr(pdf_bytes: bytes) -> str:
    """Render each PDF page to an image, then run Tesseract OCR."""
    try:
        import fitz  # PyMuPDF  # type: ignore
        from PIL import Image  # type: ignore
        import pytesseract  # type: ignore

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages: list[str] = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Render at 2× scale for better OCR accuracy
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pages.append(pytesseract.image_to_string(img))
        doc.close()
        return "\n".join(pages)
    except ImportError as exc:
        logger.error(
            "OCR fallback unavailable — missing dependency: %s. "
            "Ensure PyMuPDF, Pillow, and Tesseract are installed.",
            exc,
        )
        return ""
    except Exception as exc:
        logger.error("OCR extraction failed: %s", exc)
        return ""


# ---------------------------------------------------------------------------
# Biomarker parsing
# ---------------------------------------------------------------------------

# Each entry is (biomarker_key, compiled_regex).
# The regex must capture the numeric value in group 1.
_BIOMARKER_PATTERNS: list[tuple[str, re.Pattern]] = [
    (
        "glucose",
        re.compile(
            r"(?:fasting\s+)?glucose[^:\n]*?[:\s]+(\d+(?:\.\d+)?)\s*(?:mg/dl|mg%|mmol/l)?",
            re.IGNORECASE,
        ),
    ),
    (
        "hba1c",
        re.compile(
            r"hb\s*a1c[^:\n]*?[:\s]+(\d+(?:\.\d+)?)\s*%?",
            re.IGNORECASE,
        ),
    ),
    (
        "bmi",
        re.compile(
            r"\bbmi\b[^:\n]*?[:\s]+(\d+(?:\.\d+)?)",
            re.IGNORECASE,
        ),
    ),
    (
        "systolic_bp",
        re.compile(
            r"(?:systolic(?:\s+blood\s+pressure)?|blood\s+pressure)[^:\n]*?[:\s]+(\d{2,3})\s*/",
            re.IGNORECASE,
        ),
    ),
    (
        "diastolic_bp",
        re.compile(
            r"(?:diastolic(?:\s+blood\s+pressure)?|blood\s+pressure)[^:\n]*?[:\s]+\d{2,3}\s*/\s*(\d{2,3})",
            re.IGNORECASE,
        ),
    ),
    (
        "cholesterol",
        re.compile(
            r"(?:total\s+)?cholesterol[^:\n]*?[:\s]+(\d+(?:\.\d+)?)\s*(?:mg/dl)?",
            re.IGNORECASE,
        ),
    ),
]


def parse_biomarkers(text: str) -> Dict[str, Optional[float]]:
    """
    Search extracted PDF text for common lab-report biomarker values.

    Args:
        text: Raw text from ``extract_text_from_pdf``.

    Returns:
        A dict mapping biomarker names to float values (or ``None`` if the
        pattern was not found in the text).
        Keys: ``glucose``, ``hba1c``, ``bmi``, ``systolic_bp``,
              ``diastolic_bp``, ``cholesterol``.
    """
    results: Dict[str, Optional[float]] = {key: None for key, _ in _BIOMARKER_PATTERNS}

    for key, pattern in _BIOMARKER_PATTERNS:
        match = pattern.search(text)
        if match:
            try:
                results[key] = float(match.group(1))
                logger.debug("Parsed %s = %s", key, results[key])
            except (ValueError, IndexError) as exc:
                logger.warning("Could not convert parsed value for %s: %s", key, exc)

    return results
