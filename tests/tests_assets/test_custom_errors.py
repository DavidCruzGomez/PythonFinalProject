# Standard library imports
import unittest

# Local imports
from FinalProject.assets.custom_errors import (
    DatabaseError, ValidationError, WidgetError, InputValidationError,
    EmailConfigError, UserNotFoundError, EmailSendingError
)


class TestDatabaseError(unittest.TestCase):
    def test_default_message(self):
        error = DatabaseError()
        # Assert that the string representation of the error matches the expected default message
        self.assertEqual(str(error),
                         "DatabaseError: An error occurred with the database.\n"
                         " - Suggested action: Check database connectivity and logs.")

    def test_custom_message(self):
        error = DatabaseError("Custom message")
        self.assertEqual(str(error),
                         "DatabaseError: Custom message\n"
                         " - Suggested action: Check database connectivity and logs.")


class TestValidationError(unittest.TestCase):
    def test_default_message(self):
        error = ValidationError("username", "invalid_value")
        self.assertEqual(str(error),
                         "ValidationError: Validation failed.\n"
                         " - Field: username\n"
                         " - Value: invalid_value\n"
                         " - Suggested action: Check the field value and format.")


class TestWidgetError(unittest.TestCase):
    def test_default_message(self):
        error = WidgetError()
        self.assertEqual(str(error), "WidgetError: An error occurred with the widget.")


class TestInputValidationError(unittest.TestCase):
    def test_default_message(self):
        error = InputValidationError("invalid_input")
        self.assertEqual(str(error),
                         "InputValidationError: Invalid input provided in the widget.\n"
                         " - Input value: invalid_input\n"
                         " - Suggested action: Check the input value and format.")


class TestEmailConfigError(unittest.TestCase):
    def test_default_message(self):
        error = EmailConfigError("/path/to/config")
        self.assertEqual(str(error),
                         "EmailConfigError: Error in the email configuration.\n"
                         " - Configuration file: /path/to/config\n"
                         " - Suggested action: Verify the configuration file and its format.")


class TestUserNotFoundError(unittest.TestCase):
    def test_default_message(self):
        error = UserNotFoundError("user@example.com")
        self.assertEqual(str(error),
                         "UserNotFoundError: User not found for email: user@example.com\n"
                         " - Suggested action: Verify the email address and ensure"
                         " it is registered.")


class TestEmailSendingError(unittest.TestCase):
    def test_default_message(self):
        error = EmailSendingError("user@example.com")
        self.assertEqual(str(error),
                         "EmailSendingError: Failed to send the email.\n"
                         " - Email: user@example.com\n"
                         " - Suggested action: Check the email address and server configuration.")


if __name__ == '__main__':
    unittest.main()
