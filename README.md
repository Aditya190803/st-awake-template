# Wake Up Streamlit Apps

A GitHub Actions workflow and Python script to automatically wake up Streamlit apps.

## Overview

This repository contains a Python script and GitHub Actions workflow that wakes up Streamlit apps by clicking the "Wake Up" button. This is useful for keeping apps running and responsive, especially when deployed on platforms like Streamlit Cloud.

## How it works

1. The Python script first uses `curl` to fetch the app page and checks for the Streamlit sleep page using multiple markers such as `Zzzz`, the inactivity message, and the wake button. Selenium is launched only when the page looks asleep or inconclusive so it can click the wake button.
2. The GitHub Actions workflow runs the Python script on a schedule and on push events to the main branch.

## Repository contents

* `wake_up_streamlit.py`: The Python script that wakes up Streamlit apps.
* `wakeup_log.txt`: The log file where the script writes its output.
* `.github/workflows/wake_up.yml`: The GitHub Actions workflow configuration file.

## Usage

1. Add your Streamlit app URLs to the `STREAMLIT_APPS` list in `wake_up_streamlit.py`.
2. Set up the GitHub Actions workflow by copying the `.github/workflows/wake_up.yml` file to your repository.
3. Make sure to install the required dependencies, including Selenium.

## Log file

The script writes its output to `wakeup_log.txt`, which includes:

* Execution start time
* Awake, woken, and error messages for each app
* Sleep detection and wake button results
* A summary count by app state at the end of each execution

The log file is uploaded as an artifact after each workflow run.

## Schedule

The workflow runs on push events and once per hour. The script itself enforces a 10-hour minimum interval in CI with `ENFORCE_WAKE_INTERVAL=1` and `WAKE_INTERVAL_HOURS=10`, which gives you a reliable check roughly every 10 hours while keeping a safety buffer before the 12-hour sleep threshold.

For local/manual runs, interval skipping is disabled by default so each manual execution always checks apps.
For CI/scheduled runs, interval skipping is enabled with `ENFORCE_WAKE_INTERVAL=1` and `WAKE_INTERVAL_HOURS=10`.
