import unittest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QMessageBox, QLabel
from PySide6.QtCore import QTimer
from FinalProject.assets.utils import show_message, ValidatorBase, PasswordValidator, UsernameValidator

class TestUtils(unittest.TestCase):

    @patch('PySide6.QtWidgets.QMessageBox', autospec=True)  # patch the QMessageBox class
    def test_show_message(self, MockQMessageBox):
        # Create a mock instance of QMessageBox
        mock_exec = MagicMock()
        MockQMessageBox.return_value.exec = mock_exec

        # Mock setWindowTitle and setText as well
        MockQMessageBox.return_value.setWindowTitle = MagicMock()
        MockQMessageBox.return_value.setText = MagicMock()

        # Create the parent mock
        parent = MagicMock()

        # Call the show_message function
        show_message(parent, "Test Title", "Test Message")

        # Verify that exec was called once
        mock_exec.assert_called_once()

        # Verify that setWindowTitle and setText were called with the correct values
        MockQMessageBox.return_value.setWindowTitle.assert_called_once_with("Test Title")
        MockQMessageBox.return_value.setText.assert_called_once_with("Test Message")


    def test_validator_base_create_labels(self):
        requirements = ["Requirement 1", "Requirement 2"]
        validator = ValidatorBase(requirements)
        labels = validator.create_labels()
        self.assertEqual(len(labels), 2)
        for label in labels:
            self.assertEqual(label.styleSheet(), "color: red;")
            self.assertFalse(label.isVisible())


    def test_validator_base_show_hide_labels(self):
        requirements = ["Requirement 1", "Requirement 2"]
        validator = ValidatorBase(requirements)
        validator.create_labels()
        validator.show_labels()
        for label in validator.get_labels():
            self.assertTrue(label.isVisible())
        validator.hide_labels()
        for label in validator.get_labels():
            self.assertFalse(label.isVisible())


    def test_validator_base_validate_input(self):
        requirements = ["Requirement 1", "Requirement 2"]
        validator = ValidatorBase(requirements)
        validator.create_labels()
        regex_list = [(r'\d', validator.get_labels()[0]), (r'[a-z]', validator.get_labels()[1])]
        validation_status = [False, False]
        self.assertTrue(validator.validate_input("1a", regex_list, validation_status))
        self.assertEqual(validator.get_labels()[0].styleSheet(), "color: green;")
        self.assertEqual(validator.get_labels()[1].styleSheet(), "color: green;")
        self.assertTrue(validation_status[0])
        self.assertTrue(validation_status[1])


    def test_password_validator(self):
        validator = PasswordValidator()
        validator.create_labels()
        self.assertTrue(validator.validate_password("Password1@"))
        self.assertFalse(validator.validate_password("pass"))


    def test_username_validator(self):
        validator = UsernameValidator()
        validator.create_labels()
        self.assertTrue(validator.validate_username("valid.username_1"))
        self.assertFalse(validator.validate_username("invalid username"))


if __name__ == '__main__':
    unittest.main()
