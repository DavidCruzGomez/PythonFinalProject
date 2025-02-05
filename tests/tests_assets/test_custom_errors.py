"""
Unit tests for the custom error classes in the `FinalProject.assets.custom_errors` module.

This test suite validates the error messages and formats for various custom exception classes
used throughout the application. Each class represents a specific type of error
and includes tailored error messages to assist with debugging and resolution.

Key tests include:

- `TestDatabaseError`: Verifies the default and custom error messages for
the `DatabaseError` exception, ensuring it provides the correct message about
database connectivity and suggested actions.

- `TestValidationError`: Tests the `ValidationError` exception,
verifying that error messages include field and value details,
along with suggested actions to resolve the validation issue.

- `TestWidgetError`: Ensures the default message for the `WidgetError` exception
is correct, indicating,issues with the widget.

- `TestInputValidationError`: Validates that the `InputValidationError` exception
correctly includes the invalid input value and suggests actions to fix it.

- `TestEmailConfigError`: Tests the `EmailConfigError` exception to ensure
it correctly formats the error message with the path of the configuration file
and suggests actions to resolve the email configuration issue.

- `TestUserNotFoundError`: Verifies the default error message for
the `UserNotFoundError` exception, which includes the email address
that was not found, with suggestions for verification.

- `TestEmailSendingError`: Validates the default error message for
the `EmailSendingError` exception, confirming it includes the email address
that failed during the sending process and suggests actions to resolve the issue.

Each test ensures that the string representation of the error matches
the expected format and includes relevant details like the error type,
involved data (e.g., field, value, email), and suggested actions for resolution.

The tests use Python's `unittest` framework to check that the error messages
are generated correctly for each custom exception class.
"""

# Standard library imports
import unittest

# Local imports
from src.assets.custom_errors import (
    DatabaseError, ValidationError, WidgetError, InputValidationError,
    EmailConfigError, UserNotFoundError, EmailSendingError
)


class TestDatabaseError(unittest.TestCase):
    """
    Test suite for the DatabaseError class.

    This class tests the default and custom error messages for the DatabaseError exception.
    """

    def test_default_message(self) -> None:
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

    def test_custom_message(self) -> None:
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
    def test_default_message(self) -> None:
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
    def test_default_message(self) -> None:
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
    def test_default_message(self) -> None:
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
    def test_default_message(self) -> None:
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
    def test_default_message(self) -> None:
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
    def test_default_message(self) -> None:
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
