"""
Unit tests for the password recovery functionality and email handling in
the `src.windows.recovery_window` module.

This test suite verifies the behavior of the recovery window,
email configuration loading, and the process of sending recovery emails.
It also ensures proper error handling for invalid email configurations
or failures in sending recovery emails.

Key tests include:

- `test_initial_state`: Verifies the initial state of the recovery window,
ensuring the window title and email input field are set correctly
when the window is first opened.

- `test_recover_password_user_not_found`: Simulates a recovery attempt
with an email not found in the system, verifying that the correct
error message is displayed.

- `test_recover_password_success`: Verifies that when a valid user is found,
the recovery email is sent successfully and the success message is shown.

- `test_load_email_config_success`: Ensures that the email configuration is
loaded correctly from a JSON file and the required values are returned.

- `test_load_email_config_error`: Tests the scenario where loading
the email configuration fails, raising an `EmailConfigError`.

- `test_send_recovery_email_success`: Verifies that the recovery email
is sent successfully via SMTP when triggered.

- `test_send_recovery_email_failure`: Ensures that an `EmailSendingError` is
raised when there is an issue with sending the email through SMTP.

The tests use Python's `unittest` framework and mock dependencies such as
external file access and network calls to ensure accurate and isolated tests.
"""


# Standard library imports
import json
import smtplib
import unittest
from unittest.mock import patch, mock_open

# Third-party imports
from PySide6.QtWidgets import QApplication

# Local project-specific imports
from src.windows.recovery_window import RecoveryWindow, load_email_config, \
    EmailConfigError, EmailSender, EmailSendingError


class TestRecoveryWindow(unittest.TestCase):
    """
    Test suite for the RecoveryWindow and related functionality like
    email recovery, loading email configurations, and handling email sending.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the QApplication instance for testing the RecoveryWindow.
        This is required by PySide6 to initialize the widgets correctly.
        """
        cls.app = QApplication([])


    # Patches the EMAIL_CONFIG_FILE constant to use a fake path during tests.
    @patch('src.windows.recovery_window.EMAIL_CONFIG_FILE',
           'C:/Users/David/PycharmProjects/PythonProject1/src/assets/email_config.json')
    def setUp(self) -> None:
        """
        Set up the RecoveryWindow instance for each test case.
        This function is called before each individual test method is executed.
        """
        self.window = RecoveryWindow()


    def test_initial_state(self) -> None:
        """
        Test the initial state of the RecoveryWindow to ensure the window
        title and the email input field are set correctly when the window is first opened.
        """
        self.assertEqual(self.window.windowTitle(), "Password Recovery")
        self.assertEqual(self.window._email_input.text(), "")

    # Patches the show_message function, the send_recovery_email method,
    # and the get_user_by_email function for testing.
    @patch('src.windows.recovery_window.show_message')
    @patch.object(EmailSender, 'send_recovery_email')
    @patch('src.windows.recovery_window.get_user_by_email')
    def test_recover_password_user_not_found(self, mock_get_user_by_email, mock_send_recovery_email,
                                             mock_show_message) -> None:
        """
        Test the recovery process when the email provided is not found in the system.
        This test checks that the appropriate error message is displayed and
        the email input field is cleared.
        """
        # Simulate no user found with the email
        mock_get_user_by_email.return_value = None
        self.window._email_input.setText("nonexistent@example.com")

        self.window._recover_password()

        # Check if the show_message method was called with the appropriate error message
        mock_show_message.assert_called_with(self.window, "Error",
                                             "Email not found. Please try again.")

        # Ensure the email input field is cleared
        self.assertEqual(self.window._email_input.text(), "")


    # Patches the get_user_by_email function, the send_recovery_email method,
    # and the show_message function for testing.
    @patch('src.windows.recovery_window.get_user_by_email')
    @patch.object(EmailSender, 'send_recovery_email')
    @patch(
        'src.windows.recovery_window.show_message')
    def test_recover_password_success(self, mock_show_message, mock_send_recovery_email,
                                      mock_get_user_by_email) -> None:
        """
        Test the recovery process when a valid user is found.
        This test checks that the recovery email is sent successfully and
        the success message is shown to the user.
        """
        # Simulate finding a valid user
        mock_get_user_by_email.return_value = {"name": "Test User"}
        self.window._email_input.setText("test@example.com")

        self.window._recover_password()

        # Assert send_recovery_email was called with the correct arguments
        mock_send_recovery_email.assert_called_with("test@example.com", "Test User")

        # Assert show_message was called with the correct arguments
        mock_show_message.assert_called_with(self.window, "Success",
                                             "A recovery email has been sent.")


    def test_load_email_config_success(self) -> None:
        """
        Test loading the email configuration from a JSON file.
        This test ensures that the email configuration file is read correctly
        and the required values (email and password) are returned.
        """
        fake_email_config: dict[str, str] = {
            "sender_email": "sender@example.com",
            "sender_password": "password"
        }

        # Mock the file system calls to simulate the existence of the email config file
        with patch('os.path.exists', return_value=True), \
                patch('builtins.open', mock_open(read_data=json.dumps(fake_email_config))):

            # Call the actual function
            config = load_email_config()

            # Assertions
            self.assertEqual(config["sender_email"], "sender@example.com")
            self.assertEqual(config["sender_password"], "password")


    # Patches the load_email_config function to mock its behavior for testing.
    @patch('src.windows.recovery_window.load_email_config')
    def test_load_email_config_error(self, mock_load_email_config) -> None:
        """
        Test the case when loading the email configuration fails.
        This test checks that an EmailConfigError is raised when the configuration
        cannot be loaded correctly.
        """
        # Simulate an error while loading the email configuration
        mock_load_email_config.side_effect = EmailConfigError("Configuration error")

        # Ensure that the error is raised when the configuration cannot be loaded
        with self.assertRaises(EmailConfigError):
            load_email_config()


    # Patches the smtplib.SMTP class to mock email sending behavior for testing.
    @patch('src.windows.recovery_window.smtplib.SMTP')
    def test_send_recovery_email_success(self, mock_smtp) -> None:
        """
        Test sending a recovery email successfully.
        This test ensures that the email is sent through SMTP when the recovery email
        is triggered.
        """
        email_sender = EmailSender(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            sender_email="sender@example.com",
            sender_password="password"
        )

        # Mock the SMTP server object
        mock_server = mock_smtp.return_value.__enter__.return_value

        email_sender.send_recovery_email("recipient@example.com", "Test User")
        mock_server.sendmail.assert_called()


    # Patches the smtplib.SMTP class to mock SMTP server interactions for email sending tests.
    @patch('src.windows.recovery_window.smtplib.SMTP')
    def test_send_recovery_email_failure(self, mock_smtp) -> None:
        """
        Test the failure scenario for sending a recovery email.
        This test ensures that an EmailSendingError is raised when an SMTP error occurs
        while sending the email.
        """
        email_sender = EmailSender(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            sender_email="sender@example.com",
            sender_password="password"
        )

        # Simulate an SMTP exception
        mock_smtp.side_effect = smtplib.SMTPException

        # Ensure that the EmailSendingError is raised when an SMTP exception occurs
        with self.assertRaises(EmailSendingError):
            email_sender.send_recovery_email("recipient@example.com", "Test User")


if __name__ == '__main__':
    unittest.main()
    