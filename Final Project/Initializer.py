from datetime import date

start_date = date(2011, 5, 4)
end_date = date.today()
threads = 10

rates = [
    "EUR", "GBP", "USD", "DZD", "AUD", "BWP", "BND", "CAD", "CLP", "CNY", "COP", "CZK", "DKK", "HUF", "ISK", "IDR", "ILS", "KZT", "KRW", "KWD", 
    "LYD", "MYR", "MUR", "NPR", "NZD", "NOK", "OMR", "PKR", "PLN", "QAR", "RUB", "SAR", "SGD", "ZAR", "LKR", "SEK", "CHF", "THB", "TTD"
]

ratesForBase = [r for r in rates if r != "USD" and r != "EUR" and r != "GBP"]

