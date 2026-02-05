from src.text_normalizer import normalize_ocr_text

def test_normalize_euro():

    assert normalize_ocr_text("L10") == "£10"
