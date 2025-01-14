"""
Unit tests for the `unzip_file`, `setup_browser`, `download_file`,
and `rename_folder` functions in the `FinalProject.assets.download_files` module.

This test suite ensures that the main file handling and browser interaction
functions work correctly under various conditions.
Each function is tested with both valid and invalid inputs to verify
that they behave as expected.

Key tests include:

- `TestUnzipFile`: Verifies the behavior of the `unzip_file` function. This includes:
    - Handling valid ZIP files and extracting them correctly.
    - Properly rejecting invalid ZIP files (e.g., non-ZIP files).
    - Handling corrupt or broken ZIP files and raising the appropriate exceptions.

- `TestSetupBrowser`: Tests the `setup_browser` function to ensure:
    - Successful initialization of the Chrome browser.
    - Proper handling of browser initialization failures.

- `TestDownloadFile`: Simulates scenarios in the `download_file` function where:
    - No ZIP files are found, ensuring the function returns `None` in such cases.

- `TestRenameFolder`: Validates the `rename_folder` function by testing:
    - Successfully renaming a folder when it exists.
    - Returning `None` if the folder to be renamed does not exist.
    - Handling errors during the renaming process, such as `OSError`.

Each test case is designed to address normal behavior, edge cases,
and potential error conditions, ensuring that the functions are both reliable
and resilient to unexpected situations.
"""

# Standard library imports
import os
import unittest
import zipfile
from unittest.mock import patch, MagicMock

# Local project-specific imports
from FinalProject.assets.download_files import unzip_file, setup_browser, download_file, \
    rename_folder


class TestUnzipFile(unittest.TestCase):
    """
    Test suite for the `unzip_file` function in the `FinalProject.assets.download_files` module.

    This test suite verifies that the `unzip_file` function works correctly for:
    - Valid ZIP files: ensuring they are extracted successfully.
    - Invalid ZIP files: verifying the function raises an appropriate exception.
    - Corrupt ZIP files: checking that the function handles corrupt files correctly.
    """

    @patch("zipfile.ZipFile") # Mocking the ZipFile class
    @patch("zipfile.is_zipfile") # Mocking the is_zipfile function
    @patch("os.remove") # Mocking os.remove to prevent actual file deletion
    def test_unzip_file_valid(self, mock_remove, mock_is_zipfile, mock_zipfile) -> None:
        """
        Test the unzip_file function for a valid ZIP file.
        - Simulate a valid ZIP file scenario.
        - Ensure that the file is extracted correctly and then deleted.
        """
        # Arrange
        mock_is_zipfile.return_value = True  # Simulate that the file is a valid ZIP file

        # Create a mock ZipFile instance to simulate file extraction
        mock_zip = MagicMock()
        mock_zipfile.return_value = mock_zip

        # Mock the context manager behavior
        # This ensures the 'with' statement works properly
        mock_zip.__enter__.return_value = mock_zip

        # Mock the extractall method to simulate extraction behavior
        mock_zip.extractall = MagicMock()

        # Mock file paths
        zip_file_path = "test.zip"
        extract_to_folder = "test_folder"

        # Ensure the file exists in the test setup
        with patch("os.path.exists", return_value=True):
            # Act: Call the unzip_file function to test
            unzip_file(zip_file_path, extract_to_folder)

        # Assert: Verify that the mocks were called with the correct arguments
        mock_is_zipfile.assert_called_once_with(
            zip_file_path)  # Ensure is_zipfile was called with the correct file path
        mock_zip.extractall.assert_called_once_with(
            extract_to_folder)  # Ensure extractall was called with the correct target folder
        mock_remove.assert_called_once_with(
            zip_file_path)  # Ensure the zip file was removed after extraction

        print("Test for valid zip file passed.")

    @patch("zipfile.is_zipfile")
    def test_unzip_file_invalid(self, mock_is_zipfile) -> None:
        """
        Test the unzip_file function for an invalid ZIP file.
        - Simulate an invalid ZIP file scenario.
        - Ensure that a ValueError is raised.
        """
        # Arrange: Simulate that the file is not a valid ZIP file
        mock_is_zipfile.return_value = False

        # Mock file paths
        zip_file_path = "invalid_file.zip"
        extract_to_folder = "test_folder"

        # Act & Assert: Ensure that a ValueError is raised when an invalid ZIP file is provided
        with self.assertRaises(ValueError):
            unzip_file(zip_file_path, extract_to_folder)


    @patch("zipfile.is_zipfile")
    def test_unzip_file_bad_zip(self, mock_is_zipfile) -> None:
        """
        Test the unzip_file function for a corrupt ZIP file.
        - Simulate a BadZipFile scenario.
        - Ensure that the function raises a BadZipFile error.
        """
        # Arrange: Simulate that the file is a valid ZIP file, but it is corrupted
        mock_is_zipfile.return_value = True
        with patch("zipfile.ZipFile", side_effect=zipfile.BadZipFile("Bad ZIP file")):

            zip_file_path = "corrupt.zip"
            extract_to_folder = "test_folder"

            # Act & Assert: Ensure that a BadZipFile exception is raised
            with self.assertRaises(zipfile.BadZipFile):
                unzip_file(zip_file_path, extract_to_folder)

            print("Test for bad ZIP file passed.")


class TestSetupBrowser(unittest.TestCase):
    """
    Test suite for the `setup_browser` function in the `FinalProject.assets.download_files` module.

    This test suite verifies that the `setup_browser` function:
    - Starts the browser correctly when everything works as expected.
    - Handles failures when the browser cannot be started, returning `None`.
    """
    # Mocking the Chrome browser initialization
    @patch("selenium.webdriver.Chrome")
    def test_setup_browser_success(self, mock_chrome) -> None:
        """
        Test the setup_browser function to ensure the browser starts correctly.
        - Simulate the successful creation of a browser instance.
        """
        # Arrange: Create a mock driver instance
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # Act: Call the setup_browser function
        driver = setup_browser()

        # Assert: Verify that the mock browser was initialized and returned correctly
        # Ensure the returned driver is the mock driver
        self.assertEqual(driver, mock_driver)

        mock_chrome.assert_called_once()
        print("Test for browser setup passed.")

    # Mocking the Chrome browser initialization
    @patch("selenium.webdriver.Chrome")
    def test_setup_browser_failure(self, mock_chrome) -> None:
        """
        Test the setup_browser function when browser setup fails.
        - Simulate a failure scenario where the browser cannot be started.
        """
        # Arrange: Simulate an exception when initializing the Chrome driver
        mock_chrome.side_effect = Exception("Failed to start browser")

        # Act: Call the setup_browser function, expecting it to handle the error
        driver = setup_browser()

        # Assert: Ensure that None is returned when the browser setup fails
        self.assertIsNone(driver) # Ensure the returned driver is None if setup fails

        print("Test for browser setup failure passed.")


class TestDownloadFile(unittest.TestCase):
    """
    Test suite for the `download_file` function in the `FinalProject.assets.download_files` module.

    This test suite verifies the behavior of the `download_file` function:
    - When no ZIP files are found in the directory.
    - When a ZIP file is found and downloaded.
    """

    @patch("selenium.webdriver.Chrome")  # Mocking the Chrome browser initialization
    @patch("os.listdir")  # Mocking os.listdir to simulate the contents of a folder
    @patch("time.sleep", return_value=None)  # Skip the actual sleep for testing purposes
    def test_download_file_no_zip(self, mock_sleep, mock_listdir, mock_chrome) -> None:
        """
        Test the download_file function when no ZIP file is found in the folder.
        - Simulate that the directory contains no ZIP files.
        - Ensure that the function returns None, indicating no file was downloaded.
        """
        # Arrange: Create a mock driver instance and simulate the directory contents
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_listdir.return_value = ["image.jpg", "data.csv"]  # No .zip file

        # Act: Call the download_file function to simulate downloading
        driver = mock_driver
        file_name = download_file(driver)

        # Assert: Verify that no file was downloaded (None should be returned)
        self.assertIsNone(file_name)  # Ensure None is returned when no ZIP file is found

        print("Test for no ZIP file found passed.")


class TestRenameFolder(unittest.TestCase):
    """
    Test suite for the `rename_folder` function in the `FinalProject.assets.download_files` module.

    This test suite verifies the behavior of the `rename_folder` function under the following conditions:
    - Folder rename success: Verifies that the folder is renamed correctly.
    - Folder not found: Ensures that when the folder does not exist, the function returns `None`.
    - Folder rename failure: Simulates a failure in renaming and checks
        that the function handles the error properly.
    """
    @patch("os.rename")
    @patch("os.path.exists")
    def test_rename_folder_success(self, mock_exists, mock_rename) -> None:
        """
        Test the rename_folder function when renaming a folder is successful.
        - Simulate that the folder exists and is renamed correctly.
        """
        # Arrange: Simulate that the folder exists
        mock_exists.return_value = True
        original_folder = "test_folder"
        new_folder_name = "new_test_folder"

        # Act: Call the rename_folder function
        renamed_folder_path = rename_folder(original_folder, new_folder_name)

        # Assert: Verify that os.rename was called with the correct arguments
        mock_rename.assert_called_once_with(original_folder,
                                            os.path.join(os.path.dirname(original_folder),
                                                         new_folder_name))

        # Ensure that the function returns the new folder path
        self.assertEqual(renamed_folder_path,
                         os.path.join(os.path.dirname(original_folder), new_folder_name))
        print("Test for folder rename success passed.")

    @patch("os.path.exists")
    def test_rename_folder_folder_not_found(self, mock_exists) -> None:
        """
        Test the rename_folder function when the folder does not exist.
        - Simulate that the folder doesn't exist, and verify that the function returns None.
        """
        # Arrange: Simulate that the folder doesn't exist
        mock_exists.return_value = False
        original_folder = "non_existent_folder"
        new_folder_name = "new_folder"

        # Act: Call the rename_folder function
        renamed_folder_path = rename_folder(original_folder, new_folder_name)

        # Assert: Verify that the folder does not get renamed
        self.assertIsNone(renamed_folder_path)
        print("Test for folder not found passed.")

    @patch("os.rename")
    @patch("os.path.exists")
    def test_rename_folder_failure(self, mock_exists, mock_rename) -> None:
        """
        Test the rename_folder function when renaming a folder fails.
        - Simulate a failure scenario in os.rename.
        """
        # Arrange: Simulate that the folder exists
        mock_exists.return_value = True
        original_folder = "test_folder"
        new_folder_name = "new_test_folder"

        # Simulate that os.rename raises an exception
        mock_rename.side_effect = OSError("Failed to rename folder")

        # Act & Assert: Ensure that the function handles the error and returns None
        renamed_folder_path = rename_folder(original_folder, new_folder_name)
        self.assertIsNone(renamed_folder_path)
        print("Test for folder rename failure passed.")


if __name__ == "__main__":
    unittest.main()
