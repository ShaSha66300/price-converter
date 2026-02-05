import unittest
from src.price_parser import extract_prices

class TestPriceParser(unittest.TestCase):
    
    def test_extract_usd(self):
        text = "The burger is $5.50 today."
        results = extract_prices(text)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], 5.50)
        self.assertEqual(results[0]['currency'], 'USD')

    def test_extract_japanese_yen(self):
        text = "Total: 1000円"
        results = extract_prices(text)
        self.assertEqual(results[0]['value'], 1000.0)
        self.assertEqual(results[0]['currency'], 'JPY')

    def test_ignore_noise(self):
        text = "Call me at 555-0199"
        results = extract_prices(text)
        self.assertEqual(len(results), 0)

if __name__ == '__main__':

    unittest.main()
