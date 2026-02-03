from price_parser import extract_prices

text = "€12.99 $5 9,50 EUR ¥1200 120円"
print(extract_prices(text))