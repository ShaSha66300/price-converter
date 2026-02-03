

"""
    Runs OCR on an image frame and returns bounding boxes, detected text, and confidence scores.
"""


import easyocr
import cv2


# Returns OCR results as a list of tuples (bbox, text, confidence)
reader = easyocr.Reader(['en', 'ja'], gpu=False)


def read_text_from_frame(frame):
    

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = reader.readtext(rgb_frame)

    ocr_results = []
    for bbox, text, confidence in results:
        ocr_results.append((bbox, text, confidence))

    return ocr_results
