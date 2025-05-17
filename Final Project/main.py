import random
import logging
from datetime import datetime
from initializer import ratesForBase
from downloader import data_download, exchange_rate_print
from utils import directory_check

major_currencies = ["USD", "EUR", "GBP", "JPY", "CNY"]
directory_check("logs")
logging.basicConfig(filename="logs/progress.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    #base_currency = random.choice(ratesForBase)
    #print(f"Selected base currency: {base_currency}")

    start = datetime(2011, 5, 4)
    end = datetime.now()

    for base_currency in major_currencies:
        data_download(base_currency, start, end)
    #exchange_rate_print(base_currency)

if __name__ == "__main__":
    main()
