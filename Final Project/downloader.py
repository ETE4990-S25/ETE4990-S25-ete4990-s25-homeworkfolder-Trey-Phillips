import requests
import xmltodict
import json
import os
import threading
import logging
import time
import re
import pandas as pd
from datetime import datetime
from glob import glob
from initializer import URL, thread_count
from utils import date_range, directory_check

"""Download and parse XML into JSON"""

def fetch_with_retries(url, params, retries=3, delay=2):
    for i in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("text/xml"):
                raise ValueError(f"Unexpected content type: {content_type}")

            return response
        except Exception as e:
            logging.warning(f"[RETRY {i+1}] {params['base_currency']} {params['currency_date']}: {e}")
            time.sleep(delay * (2 ** i))
    raise Exception(f"Failed after {retries} retries for {params['base_currency']} {params['currency_date']}")

def data_fetch(date_str: str, base_currency: str):
    folder = f"data/{base_currency}"
    directory_check(folder)

    filename = os.path.join(folder, f"{date_str}.json")
    if os.path.exists(filename):
        logging.info(f"[SKIPPED] {filename} already exists.")
        return

    params = {
        "operation": "rates",
        "pb_id": "1775",
        "page": "historical",
        "currency_date": date_str,
        "base_currency_code": base_currency,
        "format_type": "xml"
    }
    try:
        response = fetch_with_retries(URL, params)

        try:
            data_dict = xmltodict.parse(response.text)
        except Exception as e:
            logging.warning(f"[ERROR] {base_currency} {date_str}: Failed to parse XML: {e}")
            return

        with open(filename, "w") as f:
            json.dump(data_dict, f, indent=4)

        logging.info(f"[SUCCESS] {base_currency} {date_str}")
        time.sleep(0.2)

    except Exception as e:
        logging.warning(f"[ERROR] {base_currency} {date_str}: {e}")

"""Threading download"""

def data_download(base_currency: str, start_date: datetime, end_date: datetime):
    threads = []

    for date in date_range(start_date, end_date):
        date_str = date.strftime("%Y-%m-%d")
        t = threading.Thread(target=data_fetch, args=(date_str, base_currency))
        threads.append(t)
        t.start()

        while threading.active_count() > thread_count:
            time.sleep(0.1)

    for t in threads:
        t.join()

"""Print exchange rate for currencies by date and chosen base currency. Checking to ensure json is being interpreted. 
SHOULD MOVE TO SEPARATE FILE LATER."""

def exchange_rate_print(base_currency):
    base_dir = os.path.join("data", base_currency)
    if not os.path.exists(base_dir):
        print("Directory error.")
        return

    files = sorted(os.listdir(base_dir))
    if not files:
        print("No data in files.")
        return

    print(f"\nExchange Rate Summary: {base_currency}\n")
    for filename in files:
        file_path = os.path.join(base_dir, filename)
        with open(file_path) as f:
            data = json.load(f)
            try:
                items = data['channel']['item']
                if not isinstance(items, list):
                    items = [items]
                print(f"{filename[:-5]}:")
                for rate in items:
                    target = rate.get("targetCurrency")
                    value = rate.get("exchangeRate")
                    print(f"   -> {target}: {value}")
            except Exception as e:
                print(f"Error. Could not parse {filename}: {e}.")

"""Aggregate all JSON data for EDA"""

def parse_for_EDA(data_dir="data"):
    all_data = []

    for base_path in glob(os.path.join(data_dir, "*")):
        base_currency = os.path.basename(base_path)
        for json_file in glob(os.path.join(base_path, "*.json")):
            with open(json_file, "r") as f:
                try:
                    data = json.load(f)
                    channel = data.get("channel", {})
                    items = channel.get("item", [])
                    if isinstance(items, dict):
                        items = [items]

                    pub_date_str = channel.get("pubDate")
                    date_obj = None
                    if pub_date_str:
                        try:
                            date_obj = datetime.strptime(pub_date_str, "%a, %d %b %Y")
                        except:
                            pass
                    if not date_obj:
                        title = channel.get("title", "")
                        match = re.search(r"\((\d{1,2} \w{3} \d{4})\)", title)
                        if match:
                            try:
                                date_obj = datetime.strptime(match.group(1), "%d %b %Y")
                            except:
                                continue

                    for rate in items:
                        if not isinstance(rate, dict):
                            continue
                        target = rate.get("targetCurrency")
                        raw_rate = rate.get("exchangeRate", "0").replace(",", "")
                        try:
                            exchange_rate = float(raw_rate)
                        except:
                            exchange_rate = None

                        all_data.append({
                            "date": date_obj,
                            "base_currency": base_currency,
                            "target_currency": target,
                            "exchange_rate": exchange_rate
                        })
                except Exception as e:
                    logging.warning(f"Failed to parse {json_file}: {e}")

    return pd.DataFrame(all_data, columns=["date", "base_currency", "target_currency", "exchange_rate"])
