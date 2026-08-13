import os
import time
from datetime import datetime

def wait(seconds):
    time.sleep(seconds)

def format_date(date_str, fmt="%Y-%m-%d"):
    return datetime.strptime(date_str, fmt)

def wait_for_url(page, url):
    page.wait_for_url(url)

def take_screenshot(page, name):
    path = os.path.join("reports", "screenshots", f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    page.screenshot(path=path)

def clear_local_storage(page):
    page.evaluate("localStorage.clear()")
