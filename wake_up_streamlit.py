from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from streamlit_app import STREAMLIT_APPS
import datetime

# Set up Selenium webdriver (assuming Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

# Initialize log file
log_file = open("wakeup_log.txt", "a")

# Log the current date and time
log_file.write("Execution started at: {}\n".format(datetime.datetime.now()))

# Iterate through each URL in the list
for url in STREAMLIT_APPS:
    try:
        # Navigate to the webpage
        driver.get(url)

        # Check if the wake up button is already clicked
        already_awake = "Already awake" in driver.page_source
        
        if not already_awake:
            # Find the button element by data-testid
            wakeup_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "button_button_primary__E3Mmg")))

            # Click the button to wake up the Streamlit app
            wakeup_button.click()

        # Log success or already awake
        if already_awake:
            log_file.write("App already awake at: {}\n".format(url))
        else:
            log_file.write("Successfully woke up app at: {}\n".format(url))
    except NoSuchElementException:
        # Log button not found
        log_file.write("Button not found for app at: {}\n".format(url))
    except Exception as e:
        # Log any other exceptions
        log_file.write("Error for app at {}: {}\n".format(url, str(e)))

# Close the browser
driver.quit()

# Close the log file
log_file.close()
