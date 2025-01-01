import unittest
from unittest.mock import patch, MagicMock
import os
import zipfile

# Import the functions to test
from FinalProject.assets.download_files import unzip_file, setup_browser, download_file


class TestUnzipFile(unittest.TestCase):

    @patch("zipfile.ZipFile")
    @patch("zipfile.is_zipfile")
    @patch("os.remove")
    def test_unzip_file_valid(self, mock_remove, mock_is_zipfile, mock_zipfile):
        """Test the unzip_file function for a valid ZIP file."""

        # Arrange
        mock_is_zipfile.return_value = True  # Simulate that the file is a valid ZIP file

        # Create a mock ZipFile instance
        mock_zip = MagicMock()
        mock_zipfile.return_value = mock_zip

        # Mock the context manager behavior
        mock_zip.__enter__.return_value = mock_zip  # This ensures the 'with' statement works properly

        # Mock the extractall method
        mock_zip.extractall = MagicMock()

        # Mock file paths
        zip_file_path = "test.zip"
        extract_to_folder = "test_folder"

        # Ensure the file exists in the test setup (mocking os.path.exists to return True)
        with patch("os.path.exists", return_value=True):
            # Act
            unzip_file(zip_file_path, extract_to_folder)

        # Assert
        mock_is_zipfile.assert_called_once_with(
            zip_file_path)  # Ensure is_zipfile was called with the correct file path
        mock_zip.extractall.assert_called_once_with(
            extract_to_folder)  # Ensure extractall was called with the correct target folder
        mock_remove.assert_called_once_with(
            zip_file_path)  # Ensure the zip file was removed after extraction

        print("Test for valid zip file passed.")

    @patch("zipfile.is_zipfile")
    def test_unzip_file_invalid(self, mock_is_zipfile):
        """Test the unzip_file function for an invalid ZIP file."""
        # Arrange
        mock_is_zipfile.return_value = False

        zip_file_path = "invalid_file.zip"
        extract_to_folder = "test_folder"

        # Act
        with self.assertRaises(ValueError):
            unzip_file(zip_file_path, extract_to_folder)


    @patch("zipfile.is_zipfile")
    def test_unzip_file_bad_zip(self, mock_is_zipfile):
        """Test the unzip_file function for a corrupt ZIP file."""
        # Arrange
        mock_is_zipfile.return_value = True
        with patch("zipfile.ZipFile", side_effect=zipfile.BadZipFile("Bad ZIP file")):

            zip_file_path = "corrupt.zip"
            extract_to_folder = "test_folder"

            # Act & Assert
            with self.assertRaises(zipfile.BadZipFile):
                unzip_file(zip_file_path, extract_to_folder)

            print("Test for bad ZIP file passed.")


class TestSetupBrowser(unittest.TestCase):

    @patch("selenium.webdriver.Chrome")
    def test_setup_browser_success(self, mock_chrome):
        """Test the setup_browser function to ensure the browser is started successfully."""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        driver = setup_browser()

        # Assert
        self.assertEqual(driver, mock_driver)
        mock_chrome.assert_called_once()
        print("Test for browser setup passed.")

    @patch("selenium.webdriver.Chrome")
    def test_setup_browser_failure(self, mock_chrome):
        """Test the setup_browser function when browser setup fails."""
        # Simulate the exception when trying to initialize the Chrome driver
        mock_chrome.side_effect = Exception("Failed to start browser")

        # Act
        driver = setup_browser()

        # Assert
        self.assertIsNone(driver)
        print("Test for browser setup failure passed.")


class TestDownloadFile(unittest.TestCase):


    @patch("selenium.webdriver.Chrome")
    @patch("os.listdir")
    @patch("time.sleep", return_value=None)  # Skip actual sleep for the test
    def test_download_file_no_zip(self, mock_sleep, mock_listdir, mock_chrome):
        """Test the download_file function when no ZIP file is found."""
        # Arrange
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        mock_listdir.return_value = ["image.jpg", "data.csv"]  # No .zip file

        # Simulate unsuccessful download
        driver = mock_driver
        file_name = download_file(driver)

        # Assert
        self.assertIsNone(file_name)
        print("Test for no ZIP file found passed.")


if __name__ == "__main__":
    unittest.main()
