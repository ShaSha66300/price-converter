import unittest
from unittest.mock import patch, MagicMock
from src.currency import convert_price

class TestCurrency(unittest.TestCase):

    # We "patch" the _rates object inside currency.py so we don't hit the real internet
    @patch('src.currency._rates') 
    def test_convert_price_success(self, mock_rates):
        # Configure the mock to return 1.5 when get_rate is called
        mock_rates.get_rate.return_value = 1.5 
        
        # Test: Convert 100 USD to EUR (Rate 1.5)
        result = convert_price(100, "USD", "EUR")
        
        self.assertEqual(result, 150.0)
        # Verify get_rate was actually called with right arguments
        mock_rates.get_rate.assert_called_with("USD", "EUR")

    @patch('currency._rates')
    def test_api_failure(self, mock_rates):
        # Simulate an API crash
        mock_rates.get_rate.side_effect = Exception("API Down")
        
        # Should return original value on error
        result = convert_price(100, "USD", "EUR")
        self.assertEqual(result, 100)

if __name__ == '__main__':

    unittest.main()

