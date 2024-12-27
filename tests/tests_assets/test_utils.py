"""
Unit tests for the utility functions and classes in
the `FinalProject.assets.utils` module.

This test suite ensures that various utility functions and validators
work as expected.

The tests mock necessary Qt components, such as `QMessageBox` and `QLabel`,
to verify their behavior without requiring a full graphical environment.

Key tests include:

- `test_show_message`: Verifies that `show_message` correctly uses `QMessageBox`
to display messages.

- `test_validator_base_create_labels`: Ensures `ValidatorBase` creates
validation labels with appropriate styles.

- `test_validator_base_show_hide_labels`: Confirms that `ValidatorBase` toggles
label visibility based on validation status.

- `test_validator_base_validate_input`: Verifies that `ValidatorBase` updates
label styles and validation status correctly.

- `test_password_validator`: Ensures `PasswordValidator` validates passwords
according to defined criteria.

- `test_username_validator`: Verifies that `UsernameValidator` checks usernames
against specified rules.

The tests use Python's `unittest` framework, along with mocking techniques,
to simulate and test functionality without the need
for a full graphical environment or actual user input.
"""

# Standard library imports
import unittest
from unittest.mock import MagicMock, patch

# Third-party imports
from PySide6.QtWidgets import QApplication

# Local imports
from FinalProject.assets.utils import (show_message, ValidatorBase, PasswordValidator,
                                       UsernameValidator)


class TestUtils(unittest.TestCase):
    """
    Test suite for utility functions and classes in the FinalProject.

    This class includes tests for the `show_message` function,
    `ValidatorBase`, `PasswordValidator`, and `UsernameValidator` classes.
    It uses the `unittest` framework and mocks necessary Qt components
    to perform unit testing.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup method that runs once before all tests.

        Initializes the QApplication instance required for Qt widgets
        before any tests are executed. This is necessary because Qt widgets
        require a QApplication to be created before they can be used.
        """
        # Initialize QApplication, which is required to use any Qt widget
        cls.app = QApplication([])


    @classmethod
    def tearDownClass(cls):
        """
        Teardown method that runs once after all tests.

        Quits the QApplication instance to clean up after tests are completed.
        """
        # Quit the Qt application after the tests are done
        cls.app.quit()


    @patch('FinalProject.assets.utils.QMessageBox', autospec=True)  # patch the QMessageBox class
    def test_show_message(self, MockQMessageBox):
        """
        Test the show_message function.

        This test ensures that the `QMessageBox` class is mocked properly,
        verifies that the `exec`, `setWindowTitle`, and `setText` methods
        are called with the expected arguments when `show_message` is called.
        """
        # Create a mock instance of QMessageBox
        mock_exec = MagicMock()
        MockQMessageBox.return_value.exec = mock_exec

        # Mock setWindowTitle and setText as well
        MockQMessageBox.return_value.setWindowTitle = MagicMock()
        MockQMessageBox.return_value.setText = MagicMock()

        # Create a mock for the 'parent' parameter
        parent = MagicMock()

        # Call the show_message function
        show_message(parent, "Test Title", "Test Message")

        # Verify that exec was called once
        mock_exec.assert_called_once()

        # Verify that setWindowTitle and setText were called with the correct values
        MockQMessageBox.return_value.setWindowTitle.assert_called_once_with("Test Title")
        MockQMessageBox.return_value.setText.assert_called_once_with("Test Message")


    def test_validator_base_create_labels(self):
        """
        Test the creation of validation labels in ValidatorBase.

        This test ensures that the ValidatorBase class correctly creates
        the labels for the given requirements, sets the correct style,
        and initially hides them.
        """
        requirements = ["Requirement 1", "Requirement 2"]
        validator = ValidatorBase(requirements)
        labels = validator.create_labels()

        # Verify that exactly 2 labels were created
        self.assertEqual(len(labels), 2)

        # Verify that the labels have the correct style and are initially hidden
        for label in labels:
            self.assertEqual(label.styleSheet(), "color: red;")
            self.assertFalse(label.isVisible())


    def test_validator_base_show_hide_labels(self):
        """
        Test the visibility of validation labels in ValidatorBase.

        This test checks the `show_labels` and `hide_labels` methods of the
        ValidatorBase class to ensure that the labels can be shown and hidden
        correctly. It verifies that the visibility of each label changes as expected.
        """
        requirements = ["Requirement 1", "Requirement 2"]
        validator = ValidatorBase(requirements)
        validator.create_labels()
        validator.show_labels()

        # Verify that the labels are visible
        for label in validator.get_labels():
            self.assertTrue(label.isVisible())

        # Hide the labels
        validator.hide_labels()

        # Verify that the labels are hidden
        for label in validator.get_labels():
            self.assertFalse(label.isVisible())


    def test_validator_base_validate_input(self):
        """
        Test the input validation functionality of ValidatorBase.

        This test ensures that the `validate_input` method correctly validates
        the input against a list of regular expressions, updates the validation
        status, and changes the label styles to green when validation succeeds.
        """
        requirements = ["Requirement 1", "Requirement 2"]
        validator = ValidatorBase(requirements)
        validator.create_labels()

        # List of regular expressions and the corresponding labels
        regex_list = [(r'\d', validator.get_labels()[0]), (r'[a-z]', validator.get_labels()[1])]

        validation_status = [False, False]

        # Call the validation method with an input that matches both regular expressions
        self.assertTrue(validator.validate_input("1a", regex_list, validation_status))

        # Verify that the labels' color changed to green (validated)
        self.assertEqual(validator.get_labels()[0].styleSheet(), "color: green;")
        self.assertEqual(validator.get_labels()[1].styleSheet(), "color: green;")

        # Verify that the validation status was updated
        self.assertTrue(validation_status[0])
        self.assertTrue(validation_status[1])


    def test_password_validator(self):
        """
        Test the password validation functionality of PasswordValidator.

        This test ensures that the `PasswordValidator` class correctly validates
        a password by checking if it matches the expected pattern. It tests both
        a valid password and an invalid one.
        """
        validator = PasswordValidator()
        validator.create_labels()

        # Verify that a valid password passes the validation
        self.assertTrue(validator.validate_password("Password1@"))

        # Verify that an invalid password (too simple) fails the validation
        self.assertFalse(validator.validate_password("pass"))


    def test_username_validator(self):
        """
        Test the username validation functionality of UsernameValidator.

        This test ensures that the `UsernameValidator` class correctly validates
        a username by checking if it matches the expected pattern. It tests both
        a valid username and an invalid one.
        """
        validator = UsernameValidator()
        validator.create_labels()

        # Verify that a valid username passes the validation
        self.assertTrue(validator.validate_username("valid.username_1"))

        # Verify that an invalid username fails the validation
        self.assertFalse(validator.validate_username("invalid username"))


if __name__ == '__main__':
    unittest.main()
