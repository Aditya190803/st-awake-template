name: Wake Up Streamlit Apps

on:
  push:
    branches:
      - main
  schedule:
    - cron: "0 0 * * *"

jobs:
  wake-up:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          pip install selenium

      - name: Run Python script to wake up Streamlit apps
        run: python wake_up_streamlit.py

      - name: Upload log file as artifact
        uses: actions/upload-artifact@v4
        with:
          name: wakeup-log
          path: wakeup_log.txt
