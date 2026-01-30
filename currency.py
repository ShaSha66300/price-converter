

"""Currency conversion utilities using forex-python."""


from forex_python.converter import CurrencyRates

_rates = CurrencyRates()


def convert_price(value, source_currency, target_currency):
    try:
        rate = _rates.get_rate(source_currency, target_currency)
        return value * rate
    except Exception as e:
        print(f"Conversion error {source_currency}->{target_currency}: {e}")
        return value