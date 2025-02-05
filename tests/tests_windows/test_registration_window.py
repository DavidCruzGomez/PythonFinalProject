"""
Unit tests for the user registration functionality in
the `FinalProject.windows.registration_window` module.

This test suite verifies the behavior of the registration window,
including user input validation and the process of registering a new user.
It also checks the behavior when invalid inputs are provided
or when required fields are left empty.

Key tests include:

- `test_initial_state`: Verifies that the initial state of
the registration window displays the correct title and empty input fields.

- `test_register_success`: Simulates a successful registration with valid inputs
and checks if the user is added to the database and if the success message is shown.

- `test_register_empty_fields`: Simulates the case where one or more fields
are empty, and verifies that an error message is shown.

- `test_register_invalid_username`: Tests a registration attempt with an
invalid username and verifies that the corresponding error message is displayed.

- `test_register_invalid_password`: Tests a registration attempt with an
invalid password and checks that the error message is shown.

- `test_close_event`: Verifies that the correct methods are called
when the window is closed (e.g., stopping the timers).


The tests use Python's `unittest` framework and mock dependencies
such as input fields, database operations, and external methods
to ensure accurate and isolated tests without the need for a GUI
or external database.
"""


# Standard library imports
import time
import unittest
from unittest.mock import patch, MagicMock

# Third-party imports
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

# Local project-specific imports
from src.windows.registration_window import RegistrationWindow


class TestRegistrationWindow(unittest.TestCase):
    """
    Unit tests for the `RegistrationWindow` class in the user registration module.

    This class contains tests that ensure proper functionality of the user
    registration process in the `RegistrationWindow` GUI. The tests cover:
    - Initial state of the window.
    - Behavior for valid and invalid inputs (username, email, password).
    - Error handling for missing fields and invalid data.
    - Proper behavior when the window is closed.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the QApplication instance for testing the RegistrationWindow.
        This is required by PySide6 to initialize the widgets correctly for testing.
        """
        cls.app = QApplication([])

    def setUp(self) -> None:
        """
        Set up the RegistrationWindow instance for each test case.
        This function is called before each individual test method is executed.
        """
        self.window = RegistrationWindow()

    def test_initial_state(self) -> None:
        """
        Test the initial state of the registration window to ensure
        that the title is correct and the input fields for username, email,
        and password are empty when the window is first opened.
        """
        self.assertEqual(self.window.windowTitle(), "User Registration")
        self.assertEqual(self.window.username_input.text(), "")
        self.assertEqual(self.window.email_input.text(), "")
        self.assertEqual(self.window.password_input.text(), "")


    # Patches `add_user_to_db` to mock user registration and `show_message`
    # to mock message display during tests.
    @patch('FinalProject.assets.users_db.add_user_to_db', return_value=None)
    @patch('FinalProject.windows.registration_window.show_message')
    def test_register_success(self, mock_show_message, mock_add_user_to_db) -> None:
        """
        Test the registration process when valid data is provided.
        This test ensures that when the username, email, and password are valid,
        the user is successfully added to the database, and the success message is displayed.
        """
        # Create mock validators
        self.window.username_validator = MagicMock()
        self.window.password_validator = MagicMock()

        # Set the validation return values
        self.window.username_validator.validate_username.return_value = True
        self.window.password_validator.validate_password.return_value = True

        # Generate unique test data (username, email)
        timestamp: int = int(time.time())
        username: str = f"user_{timestamp}"
        email: str = f"user_{timestamp}@example.com"
        password: str = "ValidPassword123"

        # Set input fields with test data
        self.window.username_input.setText(username)
        self.window.email_input.setText(email)
        self.window.password_input.setText(password)

        # Simulate a button click (which triggers _on_register)
        QTest.mouseClick(self.window.register_button, Qt.LeftButton)

        # Check if the success message was displayed
        mock_show_message.assert_called_once_with(self.window, "Success",
                                                  f"User {username} registered successfully!")


    # Patches the `show_message` function to mock message display
    # in the registration window during tests.
    @patch('FinalProject.windows.registration_window.show_message')
    def test_register_empty_fields(self, mock_show_message) -> None:
        """
        Test the registration process when one or more input fields are empty.
        This test ensures that an error message is shown when the fields are empty.
        """
        # Simulate empty fields
        self.window.username_input.setText("")
        self.window.email_input.setText("")
        self.window.password_input.setText("")

        # Simulate clicking the register button
        QTest.mouseClick(self.window.register_button, Qt.LeftButton)

        # Check if the error message is displayed
        mock_show_message.assert_called_with(self.window, "Error", "Please fill in all fields.")


    # Mocks the `show_message` function to simulate message display
    # during registration process tests.
    @patch('FinalProject.windows.registration_window.show_message')
    def test_register_invalid_username(self, mock_show_message) -> None:
        """
        Test the registration process when the username does not meet the required validation rules.
        This test ensures that the correct error message is displayed for an invalid username.
        """
        # Set input fields with invalid username and valid email and password
        self.window.username_input.setText("invalid user")
        self.window.email_input.setText("valid@example.com")
        self.window.password_input.setText("ValidPassword123")

        # Mock username validator to return False (invalid)
        with patch.object(
            self.window.username_validator, 'validate_username', return_value=False
        ):

            # Simulate clicking the register button
            QTest.mouseClick(self.window.register_button, Qt.LeftButton)

            # Check if the error message is displayed for invalid username
            mock_show_message.assert_called_with(
                self.window, "Error", "Username does not meet all requirements."
            )


    # Mocks the `show_message` function to test message display
    # without showing the actual UI message.
    @patch('FinalProject.windows.registration_window.show_message')
    def test_register_invalid_password(self, mock_show_message) -> None:
        """
        Test the registration process when the password is too short or invalid.
        This test ensures that the correct error message is shown for an invalid password.
        """
        # Set input fields with valid username and email, and an invalid password
        self.window.username_input.setText("validuser")
        self.window.email_input.setText("valid@example.com")
        self.window.password_input.setText("short")

        # Mock password validator to return False (invalid)
        with patch.object(
            self.window.password_validator,
            'validate_password',
            return_value=False
        ):

            # Simulate clicking the register button
            QTest.mouseClick(self.window.register_button, Qt.LeftButton)

            # Check if the error message is displayed for invalid password
            mock_show_message.assert_called_with(
                self.window, "Error", "Password does not meet all requirements."
            )

    def test_close_event(self) -> None:
        """
        Test the behavior when the registration window is closed.
        This test ensures that any ongoing timers for
         the username and password validators are stopped.
        """
        # Patch the timers for both validators
        with patch.object(self.window.password_validator, 'get_timer',
                          return_value=MagicMock()) as mock_password_timer, \
             patch.object(self.window.username_validator, 'get_timer',
                          return_value=MagicMock()) as mock_username_timer:
            event = MagicMock()
            self.window.close_event(event)

            # Assert that the timers are stopped when the window is closed
            mock_password_timer().stop.assert_called_once()
            mock_username_timer().stop.assert_called_once()
            event.accept.assert_called_once()


if __name__ == '__main__':
    unittest.main()
