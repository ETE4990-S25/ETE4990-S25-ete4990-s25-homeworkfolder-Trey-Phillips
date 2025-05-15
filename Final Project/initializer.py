rates = [
    "EUR", "GBP", "USD", "DZD", "AUD", "BWP", "BND", "CAD", "CLP", "CNY", "COP", "CZK", "DKK", "HUF", "ISK", "IDR", "ILS", "KZT", "KRW", "KWD", 
    "LYD", "MYR", "MUR", "NPR", "NZD", "NOK", "OMR", "PKR", "PLN", "QAR", "RUB", "SAR", "SGD", "ZAR", "LKR", "SEK", "CHF", "THB", "TTD"
]

ratesForBase = [r for r in rates if r not in ("USD", "EUR", "GBP")]
URL = "https://www.floatrates.com/historical-exchange-rates.html"
thread_count = 10
