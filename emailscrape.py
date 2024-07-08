import time
from PIL import Image
import numpy as np  # Import numpy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
from selenium.webdriver.common.keys import Keys
import ocr_module as ocr
import icecream as i


def scrape_mail_from_mca(x):
    try:
        options = webdriver.ChromeOptions()
        # Adding argument to disable the AutomationControlled flag
        options.add_argument("--disable-blink-features=AutomationControlled")
        # Exclude the collection of enable-automation switches
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # Turn-off userAutomationExtension
        options.add_experimental_option("useAutomationExtension", False)
        options.headless = True
        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

        i.ic("Opening chrome")
        driver.get(
            "https://www.mca.gov.in/content/mca/global/en/mca/master-data/MDS.html"
        )

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captchaModal"))
        )

        # Find the captcha canvas element
        canvas = driver.find_element(By.ID, "captchaCanvas")

        # Capture the screenshot of the captcha canvas
        canvas_screenshot = canvas.screenshot_as_png
        image = Image.open(BytesIO(canvas_screenshot))

        i.ic("Saving the screenshot.....")
        # Save screenshot for verification (optional)
        image.save("captcha_screenshot.png")

        i.ic("Sending Screenshot to ocr module to read text")
        captcha_text = ocr.process_screenshot("captcha_screenshot.png")

        i.ic("evaluating the output")
        captcha_solution = eval(captcha_text)

        # Wait until the captcha input field is visible and clickable
        captcha_input = driver.find_element(By.ID, "customCaptchaInput")

        captcha_input.send_keys(str(captcha_solution))  # Enter the captcha solution

        # Introduce a delay (1 second) before clicking the submit button

        # time.sleep(5)
        # Find and click the Submit button
        submit_button = driver.find_element(By.ID, "check")
        submit_button.click()

        cin = x
        search_bar = driver.find_element(By.ID, "masterdata-search-box")
        search_bar.send_keys(cin)
        search_bar.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captchaModal"))
        )
        # Find the captcha canvas element
        canvas = driver.find_element(By.ID, "captchaCanvas")

        # Capture the screenshot of the captcha canvas
        canvas_screenshot = canvas.screenshot_as_png
        image = Image.open(BytesIO(canvas_screenshot))

        i.ic("Saving the screenshot.....")
        # Save screenshot for verification (optional)
        image.save("captcha_screenshot.png")

        i.ic("Sending Screenshot to ocr module to read text")
        captcha_text = ocr.process_screenshot("captcha_screenshot.png")

        i.ic("evaluating the output")
        captcha_solution = eval(captcha_text)

        # Wait until the captcha input field is visible and clickable
        captcha_input = driver.find_element(By.ID, "customCaptchaInput")

        captcha_input.send_keys(str(captcha_solution))  # Enter the captcha solution

        # Introduce a delay (1 second) before clicking the submit button

        # time.sleep(5)
        # Find and click the Submit button
        submit_button = driver.find_element(By.ID, "check")
        submit_button.click()
        # Introduce a delay (50 seconds) to observe the result

        time.sleep(1)

        select_comp = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "company-id"))
        )
        select_comp.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captchaModal"))
        )
        # Find the captcha canvas element
        canvas = driver.find_element(By.ID, "captchaCanvas")

        # Capture the screenshot of the captcha canvas
        canvas_screenshot = canvas.screenshot_as_png
        image = Image.open(BytesIO(canvas_screenshot))

        i.ic("Saving the screenshot.....")
        # Save screenshot for verification (optional)
        image.save("captcha_screenshot.png")

        i.ic("Sending Screenshot to ocr module to read text")
        captcha_text = ocr.process_screenshot("captcha_screenshot.png")

        i.ic("evaluating the output")
        captcha_solution = eval(captcha_text)

        # Wait until the captcha input field is visible and clickable
        captcha_input = driver.find_element(By.ID, "customCaptchaInput")

        captcha_input.send_keys(str(captcha_solution))  # Enter the captcha solution

        # Introduce a delay (1 second) before clicking the submit button

        # time.sleep(5)
        # Find and click the Submit button
        submit_button = driver.find_element(By.ID, "check")
        submit_button.click()

        email_field = driver.find_element(By.ID, "emailId")

        email_value = email_field.text
        return email_value

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None

    finally:
        driver.quit()


# Example usage:
if __name__ == "__main__":
    x = "U55101TN2024PTC171539"
    resutl = scrape_mail_from_mca(x)
    print(resutl)
