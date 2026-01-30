

"""
    Static image OCR price detection.

    Loads a single image from disk, runs OCR once,
    extracts detected prices, converts currencies,
    and displays the annotated result.
"""


import re
import cv2
from ocr import read_text_from_frame
from price_parser import contains_japanese, extract_prices
from currency import convert_price


# -------------------------
# CONFIG
# -------------------------

IMAGE_PATH = "images/mercari.jpg"
TARGET_CURRENCY = "EUR"

DEFAULT_SOURCE_CURRENCY = "JPY"  # used if no currency detected

MIN_CONFIDENCE = 0.3

# Manual override:
# Set to None to disable
FORCE_SOURCE_CURRENCY = "JPY"

MIN_PRICE_VALUE = 10  # ignore prices below this (in source currency)

# -----------------------------------------------------------------------------


def resize_for_display(image, max_width=1200, max_height=800):
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)


def clean_raw_price(raw: str) -> str:
    """
    Remove OCR placeholder noise like '???' from displayed prices.
    """
    return raw.replace("?", "").strip()


def ascii_safe_label(label: str) -> str:
    replacements = {
        "€": "EUR ",
        "$": "USD ",
        "¥": "JPY ",
        "￥": "JPY ",
        "円": "JPY",
        "→": "->"
    }
    for k, v in replacements.items():
        label = label.replace(k, v)
    return label


def main():

    """
        Main execution loop:
        - Capture frame
        - Run OCR on demand
        - Extract and convert prices
        - Overlay results
    """

    image = cv2.imread(IMAGE_PATH)

    if image is None:
        print(f"Error: Could not load image: {IMAGE_PATH}")
        return

    print("Running OCR on static image...")
    ocr_results = read_text_from_frame(image)

    if not ocr_results:
        print("No text detected.")
        return


    print(f"Detected {len(ocr_results)} text regions")

    for bbox, text, confidence in ocr_results:

        # Drop low-confidence OCR early
        if confidence < MIN_CONFIDENCE:
            continue

        # Skip pure Japanese text without digits
        if contains_japanese(text) and not re.search(r'\d', text):
            continue

        prices = extract_prices(
            text,
            default_currency=DEFAULT_SOURCE_CURRENCY
        )

        # Apply manual currency override
        if FORCE_SOURCE_CURRENCY:
            for p in prices:
                p["currency"] = FORCE_SOURCE_CURRENCY

        # Filter out small values (noise)
        prices = [
            p for p in prices
            if p["value"] >= MIN_PRICE_VALUE
        ]

        for price in prices:
            converted = convert_price(
                price["value"],
                price["currency"],
                TARGET_CURRENCY
            )

            raw_clean = clean_raw_price(price["raw"])
            conf_pct = int(confidence * 100)

            label = f"{raw_clean} → {converted:.2f} {TARGET_CURRENCY} ({conf_pct}%)"
            print(label)



            # Overlay OCR detection box on frame
            pts = [(int(p[0]), int(p[1])) for p in bbox]
            for i in range(4):
                cv2.line(image, pts[i], pts[(i + 1) % 4], (0, 153, 76), 2)

            # Draw label
            safe_label = ascii_safe_label(label)

            cv2.putText(
                image,
                safe_label,
                (pts[0][0], max(20, pts[0][1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 153, 76),
                2
            )

    display_image = resize_for_display(image)
    cv2.imshow("Static OCR Result", display_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()