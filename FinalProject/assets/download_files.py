# Standard library imports
import os
import time
import zipfile

# Third-party imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def unzip_file(zip_file_path, extract_to_folder):
    try:
        if zipfile.is_zipfile(zip_file_path):
            # Unzip the file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_folder)
                print(f"The ZIP file has been extracted to: {extract_to_folder}")

            # Delete the ZIP file after extraction
            os.remove(zip_file_path)
            print(f"The ZIP file {zip_file_path} has been deleted.")
        else:
            print(f"Invalid ZIP file not found: {zip_file_path}")
    except Exception as gen_err:
        print(f"Error while extracting or deleting the file: {str(gen_err)}")

# Project path
project_path = os.getcwd()

# Browser configuration
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": project_path,
    "download.prompt_for_download": False,  # Automatically download
    "safebrowsing.enabled": True  # Avoid blocking suspicious files
}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

# Open Kaggle
driver.get("https://www.kaggle.com/")

# Log in manually
input("Please log in to Kaggle and then press Enter to continue.")

# Navigate to the desired dataset
driver.get("https://www.kaggle.com/datasets/jocelyndumlao/impulse-buying-factors-on-tiktok-shop")

# Attempt to download the file
try:
    # Wait for the download button to be clickable using the correct selector
    wait = WebDriverWait(driver, 20)
    download_button = wait.until(
        ec.element_to_be_clickable((By.XPATH, "//span[text()='Download']/ancestor::button"))
    )
    download_button.click()  # Click to open the dropdown menu

    # Wait for the dropdown menu to load and for the download option to become visible
    download_zip_option = wait.until(
        ec.element_to_be_clickable((By.XPATH, "//p[text()='Download dataset as zip']"))
    )
    download_zip_option.click()  # Click on "Download dataset as zip"

    print(f"File downloaded to the project folder: {project_path}")

    # Wait for the file to download
    time.sleep(10)  # Adjust this time based on the size of the file

    # Check if the file is in the directory
    files_in_directory = os.listdir(project_path)
    print("Files in the project folder:", files_in_directory)

    # Find the downloaded ZIP file (the most recently downloaded file)
    zip_file = [file for file in files_in_directory if file.endswith('.zip')][0]
    zip_file_path = os.path.join(project_path, zip_file)

    # Unzip the file
    unzip_file(zip_file_path, project_path)

except Exception as gen_err:
    print("Error while attempting to download the file:", str(gen_err))
finally:
    # Close the browser
    driver.quit()
