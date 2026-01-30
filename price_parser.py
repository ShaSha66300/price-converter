
"""
Extract price-like patterns from OCR text and associate them with detected or default currencies.
"""

import re

CURRENCY_MAP = {
    "€": "EUR",
    "$": "USD",
    "£": "GBP",
    "¥": "JPY",
    "￥": "JPY",
    "円": "JPY",
    "EUR": "EUR",
    "USD": "USD",
    "GBP": "GBP",
    "JPY": "JPY",
}

# Currency BEFORE number (symbols + codes)
CURRENCY_BEFORE_PATTERN = re.compile(
    r"(€|\$|£|¥|￥|EUR|USD|GBP|JPY)\s*(\d+(?:[.,]\d{1,2})?)",
    re.IGNORECASE
)

# Currency AFTER number (codes + 円)
CURRENCY_AFTER_PATTERN = re.compile(
    r"(\d+(?:[.,]\d{1,2})?)\s*(EUR|USD|GBP|JPY|円)",
    re.IGNORECASE
)


def normalize_number(num_str: str) -> float:
    return float(num_str.replace(",", ""))


def clean_raw(raw):
    # Remove leading non-currency
    return re.sub(r"^[^0-9€$£¥￥円]+", "", raw).strip()


def extract_prices(text, default_currency=None):

    """
        Extract price patterns from OCR text.

        Steps:
        1. Detect currency-before-number patterns
        2. Detect currency-after-number patterns
        3. Optionally detect bare numbers using a default currency
        4. Deduplicate results
    """
    
    results = []
    seen = set()

    for match in CURRENCY_BEFORE_PATTERN.finditer(text):
        raw = clean_raw(match.group(0))
        symbol = match.group(1)
        number = match.group(2)

        value = normalize_number(number)
        currency = CURRENCY_MAP.get(symbol.upper())

        key = (value, currency)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "value": value,
            "currency": currency,
            "raw": raw
        })

    for match in CURRENCY_AFTER_PATTERN.finditer(text):
        raw = clean_raw(match.group(0))
        number = match.group(1)
        symbol = match.group(2)

        value = normalize_number(number)
        currency = CURRENCY_MAP.get(symbol.upper())

        key = (value, currency)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "value": value,
            "currency": currency,
            "raw": raw
        })

    if default_currency:
        bare_number_pattern = re.compile(r"\b\d+(?:[.,]\d{1,2})?\b")
        for match in bare_number_pattern.finditer(text):
            raw = match.group(0)
            value = normalize_number(raw)

            key = (value, default_currency)
            if key in seen:
                continue
            seen.add(key)

            results.append({
                "value": value,
                "currency": default_currency,
                "raw": raw
            })

    return results



# To recognize Japanese text not as numbers
def contains_japanese(text):
    for ch in text:
        if (
            '\u3040' <= ch <= '\u309F' or  # Hiragana
            '\u30A0' <= ch <= '\u30FF' or  # Katakana
            '\u4E00' <= ch <= '\u9FFF'     # Kanji
        ):
            return True
    return False