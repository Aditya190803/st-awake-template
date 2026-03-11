import datetime
import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from streamlit_app import STREAMLIT_APPS

WAKE_BUTTON_TEXT = "Yes, get this app back up!"
HTTP_TIMEOUT_SECONDS = 10
BROWSER_TIMEOUT_SECONDS = 15
HTTP_MAX_RETRIES = int(os.getenv("HTTP_MAX_RETRIES", "2"))
BROWSER_MAX_RETRIES = int(os.getenv("BROWSER_MAX_RETRIES", "2"))
RETRY_BACKOFF_SECONDS = float(os.getenv("RETRY_BACKOFF_SECONDS", "2"))
WAKE_INTERVAL_HOURS = float(os.getenv("WAKE_INTERVAL_HOURS", "0"))
STATE_FILE = os.getenv("WAKE_STATE_FILE", "wakeup_state.json")


def is_sleeping_via_http(url: str) -> bool:
    for attempt in range(HTTP_MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=HTTP_TIMEOUT_SECONDS)
            response.raise_for_status()
            return WAKE_BUTTON_TEXT in response.text
        except Exception:
            if attempt >= HTTP_MAX_RETRIES:
                raise
            time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))


def wake_with_browser(url: str, log_file) -> None:
    for attempt in range(BROWSER_MAX_RETRIES + 1):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            WebDriverWait(driver, BROWSER_TIMEOUT_SECONDS).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            button = WebDriverWait(driver, BROWSER_TIMEOUT_SECONDS).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[text()='{WAKE_BUTTON_TEXT}']"))
            )
            button.click()
            log_file.write(f"[{datetime.datetime.now()}] Woke up app at: {url}\n")
            return
        except TimeoutException:
            if attempt >= BROWSER_MAX_RETRIES:
                log_file.write(f"[{datetime.datetime.now()}] Wake button not found for app at: {url}\n")
                return
            time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))
        finally:
            driver.quit()


def should_run_interval(log_file) -> bool:
    if WAKE_INTERVAL_HOURS <= 0:
        return True
    if not os.path.exists(STATE_FILE):
        return True
    try:
        with open(STATE_FILE, "r") as state_file:
            state = json.load(state_file)
        last_run = datetime.datetime.fromisoformat(state.get("last_run_utc"))
        elapsed = datetime.datetime.utcnow() - last_run
        if elapsed.total_seconds() < WAKE_INTERVAL_HOURS * 3600:
            log_file.write(
                f"[{datetime.datetime.now()}] Skipping run; last run {elapsed} ago\n"
            )
            return False
    except Exception:
        return True
    return True


def write_state() -> None:
    state = {"last_run_utc": datetime.datetime.utcnow().isoformat()}
    with open(STATE_FILE, "w") as state_file:
        json.dump(state, state_file)


with open("wakeup_log.txt", "a") as log_file:
    log_file.write(f"Execution started at: {datetime.datetime.now()}\n")

    if should_run_interval(log_file):
        for url in STREAMLIT_APPS:
            try:
                if is_sleeping_via_http(url):
                    wake_with_browser(url, log_file)
                else:
                    log_file.write(f"[{datetime.datetime.now()}] App already awake at: {url}\n")
            except Exception as e:
                log_file.write(f"[{datetime.datetime.now()}] Error for app at {url}: {str(e)}\n")
        write_state()
