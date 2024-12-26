# Standard library imports
import unittest

# Local imports
from FinalProject.assets.custom_errors import (
    DatabaseError, ValidationError, WidgetError, InputValidationError,
    EmailConfigError, UserNotFoundError, EmailSendingError
)


class TestDatabaseError(unittest.TestCase):
    """
    Test suite for the DatabaseError class.

    This class tests the default and custom error messages for the DatabaseError exception.
    """

    def test_default_message(self):
        """
        Test the default message for the DatabaseError exception.

        Asserts that the string representation of the DatabaseError matches
        the expected default message.
        """
        error = DatabaseError()
        # Assert that the string representation of the error matches the expected default message
        self.assertEqual(str(error),
                         "DatabaseError: An error occurred with the database.\n"
                         " - Suggested action: Check database connectivity and logs.")

    def test_custom_message(self):
        """
        Test the custom message for the DatabaseError exception.

        Asserts that the string representation of the DatabaseError matches
        the expected custom message.
        """
        error = DatabaseError("Custom message")
        self.assertEqual(str(error),
                         "DatabaseError: Custom message\n"
                         " - Suggested action: Check database connectivity and logs.")


class TestValidationError(unittest.TestCase):
    """
    Test suite for the ValidationError class.

    This class tests the error message format for the ValidationError exception, which includes the
    field and value information involved in the validation failure.
    """
    def test_default_message(self):
        """
        Test the default message for the ValidationError exception.

        Asserts that the string representation of the ValidationError matches
        the expected default message with the field and value details.
        """
        error = ValidationError("username", "invalid_value")
        self.assertEqual(str(error),
                         "ValidationError: Validation failed.\n"
                         " - Field: username\n"
                         " - Value: invalid_value\n"
                         " - Suggested action: Check the field value and format.")


class TestWidgetError(unittest.TestCase):
    """
    Test suite for the WidgetError class.

    This class tests the default error message for the WidgetError exception.
    """
    def test_default_message(self):
        """
        Test the default message for the WidgetError exception.

        Asserts that the string representation of the WidgetError matches
        the expected default message.
        """
        error = WidgetError()
        self.assertEqual(str(error), "WidgetError: An error occurred with the widget.")


class TestInputValidationError(unittest.TestCase):
    """
    Test suite for the InputValidationError class.

    This class tests the error message format for the InputValidationError exception, which includes
    the input value causing the validation issue.
    """
    def test_default_message(self):
        """
        Test the default message for the InputValidationError exception.

        Asserts that the string representation of the InputValidationError matches
        the expected message, including the invalid input value.
        """
        error = InputValidationError("invalid_input")
        self.assertEqual(str(error),
                         "InputValidationError: Invalid input provided in the widget.\n"
                         " - Input value: invalid_input\n"
                         " - Suggested action: Check the input value and format.")


class TestEmailConfigError(unittest.TestCase):
    """
    Test suite for the EmailConfigError class.

    This class tests the default error message for the EmailConfigError exception, which includes
    the configuration file path that caused the issue.
    """
    def test_default_message(self):
        """
        Test the default message for the EmailConfigError exception.

        Asserts that the string representation of the EmailConfigError matches the expected message
        with the configuration file details.
        """
        error = EmailConfigError("/path/to/config")
        self.assertEqual(str(error),
                         "EmailConfigError: Error in the email configuration.\n"
                         " - Configuration file: /path/to/config\n"
                         " - Suggested action: Verify the configuration file and its format.")


class TestUserNotFoundError(unittest.TestCase):
    """
    Test suite for the UserNotFoundError class.

    This class tests the default error message for the UserNotFoundError exception, which includes
    the email address that was not found in the system.
    """
    def test_default_message(self):
        """
        Test the default message for the UserNotFoundError exception.

        Asserts that the string representation of the UserNotFoundError matches the expected message
        with the email address that was not found.
        """
        error = UserNotFoundError("user@example.com")
        self.assertEqual(str(error),
                         "UserNotFoundError: User not found for email: user@example.com\n"
                         " - Suggested action: Verify the email address and ensure"
                         " it is registered.")


class TestEmailSendingError(unittest.TestCase):
    """
    Test suite for the EmailSendingError class.

    This class tests the default error message for the EmailSendingError exception, which includes
    the email address that failed during the sending process.
    """
    def test_default_message(self):
        """
        Test the default message for the EmailSendingError exception.

        Asserts that the string representation of the EmailSendingError matches
        the expected message, including the email address that failed to send.
        """
        error = EmailSendingError("user@example.com")
        self.assertEqual(str(error),
                         "EmailSendingError: Failed to send the email.\n"
                         " - Email: user@example.com\n"
                         " - Suggested action: Check the email address and server configuration.")


if __name__ == '__main__':
    unittest.main()
