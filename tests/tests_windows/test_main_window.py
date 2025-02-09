"""
Unit tests for the login functionality and UI interactions in
the `src.windows.main_window` module.

This test suite verifies the behavior of the main window and login system,
ensuring that user interactions are handled correctly and that the application
responds with appropriate feedback for valid and invalid inputs.

Key tests include:

- `test_initial_state`: Verifies the initial state of the login window,
ensuring that the title, input fields, and feedback label are set
to their default values.

- `test_login_successful`: Tests the login functionality with valid credentials,
ensuring that the user is logged in successfully and
the appropriate method (`_login_successful`) is called.

- `test_empty_username`: Simulates a login attempt with an empty username
and verifies that the correct error message ("Username cannot be empty.")
is displayed.

- `test_empty_password`: Simulates a login attempt with an empty password
and verifies that the correct error message ("Password cannot be empty.")
is displayed.

- `test_invalid_credentials`: Tests a login attempt with an incorrect password
for a valid username and checks that the error message
"User not found. Please try again." is shown.

- `test_handle_login_error_incorrect_password`: Tests the login system
with valid username but incorrect password, ensuring that
the correct error message ("Incorrect password. Please try again.") is displayed.

- `test_open_registration_window`: Verifies that the registration window opens
correctly when the corresponding button is clicked.

- `test_open_recovery_window`: Verifies that the recovery window opens
correctly when the corresponding button is clicked.

The tests use Python's `unittest` framework to simulate user actions
and verify the UI behavior, without needing to run the application
in a graphical environment.
"""
# Standard library imports
import unittest
from unittest.mock import patch, MagicMock

# Third-party imports
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

# Local project-specific imports
from src.windows.main_window import MainWindow


class TestMainWindow(unittest.TestCase):
    """
    Unit tests for the login window in the `src.windows.main_window` module.

    This suite verifies the behavior of the login process,
    including input validation, error handling, and UI interactions such
    as opening the registration and recovery windows.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the QApplication instance for testing the MainWindow.
        This is necessary for initializing the widgets properly in PySide6.
        """
        cls.app = QApplication([])

    def setUp(self) -> None:
        """
        Set up a fresh instance of the MainWindow for each test.
        This ensures each test starts with a clean state of the window.
        """
        self.window = MainWindow()

    def test_initial_state(self) -> None:
        """
        Test to check the initial state of the main window:
        - Window title.
        - Whether the input fields (username, password) are empty.
        - Whether the feedback label is empty.
        """
        # Check if the window title is as expected
        self.assertEqual(self.window.windowTitle(), "Final project David Cruz Gómez")

        # Check if the input fields are empty initially
        self.assertEqual(self.window._username_input.text(), "")
        self.assertEqual(self.window._password_input.text(), "")

        # Check if the feedback label is empty initially
        self.assertEqual(self.window._feedback_label.text(), "")


    # Mocking the get_user_by_username function
    @patch('src.windows.main_window.get_user_by_username')
    # Mocking the get_user_by_email function
    @patch('src.windows.main_window.get_user_by_email')
    # Mocking the check_password_hash function
    @patch('src.windows.main_window.check_password_hash')
    def test_login_successful(
            self, mock_check_password_hash, mock_get_user_by_email, mock_get_user_by_username
    ) -> None:
        """
        Test to check the behavior of login when the username and password are correct.
        """
        # Simulate entering a valid username and password.
        self.window._username_input.setText("testuser")
        self.window._password_input.setText("testpassword")

        # Mock the response from get_user_by_username to return a user with a hashed password
        mock_get_user_by_username.return_value = {"password_hash": "hashed_password"}

        # Mock the password hash check to return True, indicating a correct password
        mock_check_password_hash.return_value = True

        # Mock the _login_successful method to check if it gets called after a successful login
        with patch.object(self.window, '_login_successful') as mock_login_successful:

            # Simulate clicking the login button
            QTest.mouseClick(self.window._login_button, Qt.LeftButton)

            mock_login_successful.assert_called_once()

    def test_empty_username(self) -> None:
        """
        Test that simulates a login attempt with an empty username.
        Verifies the correct message is shown.
        """
        # Set the username to empty and provide a valid password
        self.window._username_input.setText("")
        self.window._password_input.setText("testpassword")

        # Patch the setText method of the feedback label to check the message
        with patch.object(self.window._feedback_label, 'setText') as mock_set_text:

            # Simulate clicking the login button
            QTest.mouseClick(self.window._login_button, Qt.LeftButton)

            mock_set_text.assert_called_with("Username cannot be empty.")

    def test_empty_password(self) -> None:
        """
        Test that simulates a login attempt with an empty password.
        Verifies the correct message is shown.
        """
        # Set a valid username and leave the password empty
        self.window._username_input.setText("testuser")
        self.window._password_input.setText("")

        # Patch the setText method of the feedback label to check the message
        with patch.object(self.window._feedback_label, 'setText') as mock_set_text:

            # Simulate clicking the login button
            QTest.mouseClick(self.window._login_button, Qt.LeftButton)

            mock_set_text.assert_called_with("Password cannot be empty.")

    def test_invalid_credentials(self) -> None:
        """
        Test that simulates a login attempt with a valid username but an incorrect password.
        Verifies the correct "User not found" message is shown.
        """
        # Set the username and provide an incorrect password
        self.window._username_input.setText("testuser")
        self.window._password_input.setText("wrongpassword")

        # Mock the response from get_user_by_username to return None, simulating a user not found
        with patch('src.windows.main_window.get_user_by_username', return_value=None):

            # Patch the setText method of the feedback label to check the message
            with patch.object(self.window._feedback_label, 'setText') as mock_set_text:

                # Simulate clicking the login button
                QTest.mouseClick(self.window._login_button, Qt.LeftButton)

                mock_set_text.assert_called_with("User not found. Please try again.")


    # Mock the get_user_by_email function
    @patch('src.windows.main_window.get_user_by_email')
    def test_handle_login_error_incorrect_password(self, mock_get_user_by_email) -> None:
        """
        Test that simulates a login attempt with a valid username and an incorrect password.
        Verifies the correct "Incorrect password" message is shown.
        """
        # Set the username and provide an incorrect password
        self.window._username_input.setText("testuser")
        self.window._password_input.setText("wrongpassword")

        # Mock the response from get_user_by_email to return a user with a hashed password
        mock_get_user_by_email.return_value = {"password_hash": "hashed_password"}

        # Mock the password hash check to return False, simulating an incorrect password
        with patch('src.windows.main_window.check_password_hash', return_value=False):

            # Patch the setText method of the feedback label to check the message
            with patch.object(self.window._feedback_label, 'setText') as mock_set_text:

                # Simulate clicking the login button
                QTest.mouseClick(self.window._login_button, Qt.LeftButton)
                mock_set_text.assert_called_with("Incorrect password. Please try again.")


    # Patching the RegistrationWindow to simulate opening the registration window.
    @patch('src.windows.main_window.RegistrationWindow')
    def test_open_registration_window(self, MockRegistrationWindow) -> None:
        """
        Test to verify that the registration window opens correctly.
        """
        # Create a mock instance of the registration window.
        mock_window_instance = MockRegistrationWindow.return_value

        # Simulate the 'show' method.
        mock_window_instance.show = MagicMock()

        self.window._open_registration_window()
        mock_window_instance.show.assert_called_once()


    # Patching the RecoveryWindow to simulate opening the recovery window.
    @patch('src.windows.main_window.RecoveryWindow')
    def test_open_recovery_window(self, MockRecoveryWindow) -> None:
        """
        Test to verify that the password recovery window opens correctly.
        """
        # Create a mock instance of the recovery window.
        mock_window_instance = MockRecoveryWindow.return_value

        # Simulate the 'show' method.
        mock_window_instance.show = MagicMock()

        self.window._open_recovery_window()
        mock_window_instance.show.assert_called_once()


if __name__ == '__main__':
    unittest.main()
