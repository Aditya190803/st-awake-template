# Wake Up Streamlit Apps

A GitHub Actions workflow and Python script to automatically wake up Streamlit apps.

## Overview

This repository contains a Python script and GitHub Actions workflow that wakes up Streamlit apps by clicking the "Wake Up" button. This is useful for keeping apps running and responsive, especially when deployed on platforms like Streamlit Cloud.

## How it works

1. The Python script uses Selenium to navigate to each app URL, check if the "Wake Up" button is already clicked, and click it if necessary.
2. The GitHub Actions workflow runs the Python script on a schedule (daily at 12:00 AM UTC) and on push events to the main branch.

## Repository contents

* `wake_up_streamlit.py`: The Python script that wakes up Streamlit apps.
* `wakeup_log.txt`: The log file where the script writes its output.
* `.github/workflows/wake-up.yml`: The GitHub Actions workflow configuration file.

## Usage

1. Add your Streamlit app URLs to the `STREAMLIT_APPS` list in `wake_up_streamlit.py`.
2. Set up the GitHub Actions workflow by copying the `.github/workflows/wake-up.yml` file to your repository.
3. Make sure to install the required dependencies, including Selenium.

## Log file

The script writes its output to `wakeup_log.txt`, which includes:

* Execution start time
* Success or already awake messages for each app
* Button not found or error messages for each app

The log file is uploaded as an artifact after each workflow run.

## Schedule

The workflow runs daily at 12:00 AM UTC and on push events to the main branch. You can adjust the schedule in the `.github/workflows/wake-up.yml` file.
