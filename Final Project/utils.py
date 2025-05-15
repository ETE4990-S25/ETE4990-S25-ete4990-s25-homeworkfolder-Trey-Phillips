from datetime import datetime, timedelta
import os

def date_range(start_date: datetime, end_date: datetime):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days = 1)

def directory_check(path: str):
    os.makedirs(path, exist_ok = True)
