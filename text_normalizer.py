
import re

def normalize_ocr_text(text):
    """
        Post-processing utilities for OCR text.

        This module corrects common OCR misclassifications of currency symbols (e.g., 'Y' misread instead of '¥').

        Corrections are applied only when the character appears immediately before a digit to avoid corrupting
        normal words (e.g., 'SALE', 'SIZE'). This keeps normalization conservative and minimizes false positives.
    """

    replacements = {
        "E": "€",
        "Y": "¥",
        "L": "£",
    }

    normalized = text

    for wrong, correct in replacements.items():
        # Replace letter only when directly followed by a digit
        pattern = rf"\b{wrong}(?=\d)"
        normalized = re.sub(pattern, correct, normalized)

    return normalized