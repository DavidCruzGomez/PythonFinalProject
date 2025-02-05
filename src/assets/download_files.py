"""
Automated File Download, Extraction, and Processing Script.

This module provides a set of functions to automate downloading a dataset from Kaggle,
extracting its contents, and performing necessary post-processing tasks such as renaming
folders. The script integrates web automation using Selenium WebDriver and file operations
with Python's standard libraries.

Key Features:
-------------
1. **File Download Automation**:
   - Automates the process of logging into Kaggle and downloading a dataset ZIP file.
   - Uses Selenium WebDriver for interaction with the Kaggle website.

2. **File Extraction**:
   - Extracts the downloaded ZIP file to a specified directory.
   - Handles corrupt ZIP files or invalid paths gracefully.
   - Deletes the ZIP file after successful extraction.

3. **Folder Management**:
   - Renames the extracted folder to a user-defined name.
   - Ensures smooth error handling during the renaming process.

4. **WebDriver Configuration**:
   - Configures a Chrome WebDriver instance with download preferences to avoid
     prompts during file downloads.

Functions:
----------
1. `unzip_file(zip_file_path: str, extract_to_folder: str) -> None`:
   - Unzips a given ZIP file to the specified folder.
   - Deletes the ZIP file after successful extraction.

2. `rename_folder(folder_path: str, new_folder_name: str) -> str | None`:
   - Renames a specified folder to a new name and returns the new path.

3. `setup_browser() -> webdriver.Chrome | None`:
   - Sets up and returns a Chrome WebDriver instance with configured preferences.

4. `download_file(driver: webdriver.Chrome, sleep_time: int = 10) -> str | None`:
   - Automates the download of a dataset ZIP file from Kaggle.

Main Execution Workflow:
------------------------
1. **Setup**:
   - Initializes the Chrome WebDriver with custom preferences.

2. **Dataset Download**:
   - Automates the login to Kaggle, navigates to the dataset page, and downloads the ZIP file.

3. **File Extraction**:
   - Extracts the contents of the downloaded ZIP file.

4. **Folder Renaming**:
   - Renames the extracted folder to a user-defined name.

5. **Cleanup**:
   - Closes the WebDriver instance and handles any cleanup tasks.

Usage:
------
Execute the script directly, and follow the on-screen prompts for interaction with Kaggle.
The dataset is downloaded, extracted, and prepared automatically.
"""
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


def unzip_file(zip_file_path: str, extract_to_folder: str) -> None:
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


def rename_folder(folder_path: str, new_folder_name: str) -> str | None:
    """Renames the extracted folder."""
    try:
        parent_folder = os.path.dirname(folder_path)
        new_folder_path = os.path.join(parent_folder, new_folder_name)

        os.rename(folder_path, new_folder_path)
        print(f"Folder has been renamed to: {new_folder_name}")
        return new_folder_path
    except Exception as rename_err:
        print(f"Error renaming folder: {str(rename_err)}")
        return None


def setup_browser() -> webdriver.Chrome | None:
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


def download_file(driver: webdriver.Chrome, sleep_time: int = 10) -> str | None:
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

                # Unzip the file
                unzip_file(zip_file_path, os.getcwd())

                # After extracting, find the folder
                extracted_folder = os.path.join(os.getcwd(), "Exploring factors influencing"
                                                             " the impulse buying behavior of"
                                                             " Vietnamese students on TikTok Shop"
                                                )

                # Wait for the folder to exist
                while not os.path.exists(extracted_folder):
                    print(f"Waiting for the folder to be extracted: {extracted_folder}")
                    time.sleep(2)

                # Rename the extracted folder
                new_folder_name = "impulse_buying_data"
                renamed_folder_path = rename_folder(extracted_folder, new_folder_name)

                if renamed_folder_path:
                    print(f"Folder renamed successfully to: {new_folder_name}")
                else:
                    print("Error: The folder could not be renamed.")
            else:
                print("Error: File could not be downloaded.")
        finally:
            # Close the browser after finishing
            driver.quit()
