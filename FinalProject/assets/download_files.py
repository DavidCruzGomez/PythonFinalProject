# Standard library imports
import os
import time
import zipfile

# Third-party imports
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def unzip_file(zip_file_path, extract_to_folder):
    """Unzips the specified ZIP file into the target folder."""
    try:
        if zipfile.is_zipfile(zip_file_path):
            # Unzip the file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_folder)
                print(f"The ZIP file has been extracted to: {extract_to_folder}")

            # Delete the ZIP file after extraction
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)
                print(f"The ZIP file {zip_file_path} has been deleted.")

            else:
                print(f"Warning: The ZIP file {zip_file_path} was not found to be deleted.")

        else:
            raise ValueError(f"Error: The file {zip_file_path} is not a valid ZIP file.")

    except zipfile.BadZipFile as zip_err:
        print(f"Error: The ZIP file is corrupt: {str(zip_err)}")
        raise

    except FileNotFoundError as fnf_err:
        print(f"Error: The ZIP file was not found: {str(fnf_err)}")
        raise

    except Exception as gen_err:
        print(f"Unknown error while extracting or deleting the file: {str(gen_err)}")
        raise


def setup_browser():
    """Sets up and returns a Chrome browser with specific preferences."""
    try:
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": os.getcwd(),
            "download.prompt_for_download": False,  # Automatically download
            "safebrowsing.enabled": True  # Avoid blocking suspicious files
        }
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
        return driver


    except WebDriverException as web_err:
        print(f"Error starting the browser: {str(web_err)}")
        return None

    except Exception as gen_err:
        print(f"Unknown error while setting up the browser: {str(gen_err)}")
        return None


def download_file(driver, sleep_time=10):
    """Attempts to download the file from Kaggle."""
    try:
        driver.get("https://www.kaggle.com/")

        # Wait for the login to be completed manually, and ensure the user has logged in
        input("Please log in to Kaggle and then press Enter to continue...")

        # After login, navigate to the dataset page
        driver.get(
            "https://www.kaggle.com/datasets/jocelyndumlao/impulse-buying-factors-on-tiktok-shop")

        # Wait for the download button to be clickable
        wait = WebDriverWait(driver, 20)
        download_button = wait.until(
            ec.element_to_be_clickable((By.XPATH, "//span[text()='Download']/ancestor::button"))
        )
        download_button.click()  # Opens the dropdown menu

        # Wait for the "Download dataset as zip" option to be visible
        download_zip_option = wait.until(
            ec.element_to_be_clickable((By.XPATH, "//p[text()='Download dataset as zip']"))
        )
        download_zip_option.click()  # Click on "Download dataset as zip"

        print(f"The file will be downloaded to the working directory: {os.getcwd()}")

        # Wait for the file to download (adjust the time based on file size)
        time.sleep(sleep_time)

        # Check if the ZIP file is in the directory
        files_in_directory = os.listdir(os.getcwd())
        zip_files = [file for file in files_in_directory if file.endswith('.zip')]

        if not zip_files:
            print("Error: No ZIP file found in the directory.")
            return None

        return zip_files[0]  # Return the first ZIP file found

    except TimeoutException as time_err:
        print(f"Error: Timeout during file download: {str(time_err)}")

    except WebDriverException as web_err:
        print(f"Error: Unable to interact with the browser: {str(web_err)}")

    except Exception as gen_err:
        print(f"Unknown error while trying to download the file: {str(gen_err)}")

    return None


if __name__ == "__main__":
    # Set up the browser and download the file
    driver = setup_browser()
    if driver is None:
        print("Error: The browser could not be started. Exiting.")
    else:
        try:
            # Call the function to download the file
            zip_file = download_file(driver)
            if zip_file:
                zip_file_path = os.path.join(os.getcwd(), zip_file)
                unzip_file(zip_file_path, os.getcwd())
            else:
                print("Error: File could not be downloaded.")
        finally:
            # Close the browser after finishing
            driver.quit()
