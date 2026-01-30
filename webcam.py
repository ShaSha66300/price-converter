

"""
    Real-time webcam OCR price detection.

    Captures frames from the system camera, runs OCR on demand,
    extracts detected prices, converts currencies, and overlays
    bounding boxes and converted values onto the video stream.
"""

import cv2
from ocr import read_text_from_frame
from price_parser import extract_prices
from currency import convert_price
from text_normalizer import normalize_ocr_text
import re

MIN_CONFIDENCE = 0.15

TARGET_CURRENCY = "EUR"

# -----------------------------------------------------------------------------


def main():

    """
        Main execution loop:
        - Capture frame
        - Run OCR on demand
        - Extract and convert prices
        - Overlay results
    """

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    ocr_results = []
    price_results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Overlay OCR detection box on frame
        for bbox, text, confidence in ocr_results:
            pts = [(int(p[0]), int(p[1])) for p in bbox]

            # Drop very low confidence OCR
            if confidence < MIN_CONFIDENCE:
                continue

            # Drop pure question marks (??? noise)
            if re.fullmatch(r"\?+", text):
                continue

            # Drop text with no digits at all
            if not re.search(r"\d", text):
                continue

            for i in range(4):
                cv2.line(frame, pts[i], pts[(i + 1) % 4], (0, 255, 0), 2)

            cv2.putText(
                frame,
                text,
                (pts[0][0], pts[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            for price in price_results:
                if price["raw"] in text:
                    label = f'{price["raw"]} -> {price["converted"]:.2f} {TARGET_CURRENCY}'
                    cv2.putText(
                        frame,
                        label,
                        (pts[0][0], pts[0][1] - 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 200, 255),
                        2
                    )

        cv2.imshow("AI Camera", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("t"):
            print("Running OCR + price conversion...")
            ocr_results = read_text_from_frame(frame)

            price_results = []
            for _, text, _ in ocr_results:
                clean_text = normalize_ocr_text(text)
                prices = extract_prices(clean_text)

                for p in prices:
                    converted = convert_price(
                        p["value"],
                        p["currency"],
                        TARGET_CURRENCY
                    )

                    if converted is not None:
                        price_results.append({
                            "raw": p["raw"],
                            "converted": converted
                        })

            print(f"Detected {len(price_results)} prices")

        elif key == ord("c"):
            ocr_results.clear()
            price_results.clear()
            print("Cleared results")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()