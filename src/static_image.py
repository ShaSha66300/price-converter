"""
    Static image OCR price detection.

    Loads a single image from disk, runs OCR once,
    extracts detected prices, converts currencies using a caching mechanism,
    and displays the annotated result.

    Usage:
        python static_image.py path/to/image.jpg --target USD
"""

import argparse
import sys
import re
import cv2
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Local modules
from ocr import read_text_from_frame
from price_parser import contains_japanese, extract_prices
from currency import convert_price

def parse_arguments():
    """
    Handles command-line arguments to make the script flexible.
    """
    parser = argparse.ArgumentParser(description="OCR Price Converter CLI")
    
    # Required Argument
    parser.add_argument(
        "image_path", 
        type=str, 
        help="Path to the input image file."
    )

    # Optional Arguments
    parser.add_argument(
        "--target", 
        type=str, 
        default="EUR", 
        help="Target currency code (e.g., EUR, USD). Default: EUR"
    )
    parser.add_argument(
        "--default-source", 
        type=str, 
        default="JPY", 
        help="Default source currency if none is detected. Default: JPY"
    )
    parser.add_argument(
        "--confidence", 
        type=float, 
        default=0.3, 
        help="Minimum OCR confidence threshold (0.0 - 1.0). Default: 0.3"
    )
    parser.add_argument(
        "--force-source", 
        type=str, 
        default=None, 
        help="Force all detected prices to be this source currency (e.g., JPY)."
    )
    parser.add_argument(
        "--min-value", 
        type=float, 
        default=10.0, 
        help="Ignore prices below this value. Default: 10.0"
    )

    return parser.parse_args()


def resize_for_display(image, max_width=1200, max_height=800):
    """Resizes large images for better screen display."""
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)


def clean_raw_price(raw: str) -> str:
    """Remove OCR placeholder noise like '???'."""
    return raw.replace("?", "").strip()


def ascii_safe_label(label: str) -> str:
    """Ensure labels handle special characters gracefully."""
    replacements = {
        "€": "EUR ", "$": "USD ", "¥": "JPY ", "￥": "JPY ", 
        "円": "JPY", "→": "->"
    }
    for k, v in replacements.items():
        label = label.replace(k, v)
    return label


def get_cached_rate(source: str, target: str, cache: Dict[str, float]) -> float:
    """
    Retrieves exchange rate from cache or fetches from API if missing.
    
    HACK: Since `currency.py` only has `convert_price`, we convert 1 unit
    to discover the exchange rate, then cache it.
    """
    if source == target:
        return 1.0
    
    cache_key = f"{source}_{target}"
    
    if cache_key in cache:
        return cache[cache_key]
    
    print(f"Fetching live rate for {source} -> {target}...")
    try:
        # Convert 1.0 unit to get the raw rate
        rate = convert_price(1.0, source, target)
        if rate is None:
            rate = 0.0 # Handle failure gracefully
        cache[cache_key] = rate
        return rate
    except Exception as e:
        print(f"Warning: Could not fetch rate for {source}: {e}")
        return 0.0


def main():
    args = parse_arguments()

    # validate path
    img_path = Path(args.image_path)
    if not img_path.exists():
        print(f"Error: File not found at {img_path}")
        sys.exit(1)

    print(f"Loading image: {img_path}")
    image = cv2.imread(str(img_path))

    if image is None:
        print("Error: Could not read image data.")
        sys.exit(1)

    print("Running OCR... (This may take a moment due to EasyOCR model loading)")
    ocr_results = read_text_from_frame(image)

    if not ocr_results:
        print("No text detected.")
        sys.exit(0)

    print(f"Detected {len(ocr_results)} text regions. Processing...")

    # Initialize Rate Cache
    # Format: {'JPY_EUR': 0.006, 'USD_EUR': 0.92}
    rate_cache: Dict[str, float] = {}

    for bbox, text, confidence in ocr_results:

        if confidence < args.confidence:
            continue

        # Skip Japanese text with no numbers
        if contains_japanese(text) and not re.search(r'\d', text):
            continue

        prices = extract_prices(
            text,
            default_currency=args.default_source
        )

        # Apply override if set
        if args.force_source:
            for p in prices:
                p["currency"] = args.force_source

        # Filter small values
        prices = [p for p in prices if p["value"] >= args.min_value]

        for price in prices:
            source_curr = price["currency"]
            
            # Use cached rate logic
            rate = get_cached_rate(source_curr, args.target, rate_cache)
            
            if rate == 0.0:
                continue  # Skip if conversion failed

            converted_val = price["value"] * rate
            
            # Formatting output
            raw_clean = clean_raw_price(price["raw"])
            conf_pct = int(confidence * 100)
            label = f"{raw_clean} -> {converted_val:.2f} {args.target} ({conf_pct}%)"
            
            print(f"Match: {label}")

            # Draw Box
            pts = [(int(p[0]), int(p[1])) for p in bbox]
            for i in range(4):
                cv2.line(image, pts[i], pts[(i + 1) % 4], (0, 153, 76), 2)

            # Draw Label
            safe_text = ascii_safe_label(label)
            cv2.putText(
                image, safe_text,
                (pts[0][0], max(20, pts[0][1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 153, 76), 2
            )

    display_image = resize_for_display(image)
    cv2.imshow(f"Result - {args.target}", display_image)
    print("Press any key to close the window.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
