from price_parser import extract_prices

def test_extract_simple_price():
    text = "This costs 19.99 USD today"
    prices = extract_prices(text)
    assert len(prices) == 1
    assert prices[0]["value"] == 19.99
    assert prices[0]["currency"] == "USD"

