import unittest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication
from FinalProject.windows.registration_window import RegistrationWindow, InputValidationError, WidgetError

class TestRegistrationWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = RegistrationWindow()

    def test_initial_state(self):
        self.assertEqual(self.window.windowTitle(), "User Registration")
        self.assertEqual(self.window.username_input.text(), "")
        self.assertEqual(self.window.email_input.text(), "")
        self.assertEqual(self.window.password_input.text(), "")

    @patch('FinalProject.windows.registration_window.add_user_to_db')
    @patch(
        'FinalProject.windows.registration_window.show_message')  # Patch here instead of on self.window
    def test_register_success(self, mock_show_message, mock_add_user_to_db):
        # Set input fields with test data
        self.window.username_input.setText("validuser")
        self.window.email_input.setText("valid@example.com")
        self.window.password_input.setText("ValidPassword123")

        # Call the registration method
        self.window._on_register()

        print(mock_add_user_to_db.call_args_list)
        # Assertions
        mock_add_user_to_db.assert_called_with("validuser", "valid@example.com", "ValidPassword123")
        mock_show_message.assert_called_with(self.window, "Success",
                                             "User validuser registered successfully!")

    @patch('FinalProject.windows.registration_window.show_message')
    def test_register_empty_fields(self, mock_show_message):
        self.window.username_input.setText("")
        self.window.email_input.setText("")
        self.window.password_input.setText("")

        self.window._on_register()
        mock_show_message.assert_called_with(self.window, "Error", "Please fill in all fields.")

    @patch('FinalProject.windows.registration_window.show_message')
    def test_register_invalid_username(self, mock_show_message):
        self.window.username_input.setText("invalid user")
        self.window.email_input.setText("valid@example.com")
        self.window.password_input.setText("ValidPassword123")

        with patch.object(self.window.username_validator, 'validate_username', return_value=False):
            self.window._on_register()
            mock_show_message.assert_called_with(self.window, "Error", "Username does not meet all requirements.")

    @patch('FinalProject.windows.registration_window.show_message')
    def test_register_invalid_password(self, mock_show_message):
        self.window.username_input.setText("validuser")
        self.window.email_input.setText("valid@example.com")
        self.window.password_input.setText("short")

        with patch.object(self.window.password_validator, 'validate_password', return_value=False):
            self.window._on_register()
            mock_show_message.assert_called_with(self.window, "Error", "Password does not meet all requirements.")

    def test_close_event(self):
        with patch.object(self.window.password_validator, 'get_timer', return_value=MagicMock()) as mock_password_timer, \
             patch.object(self.window.username_validator, 'get_timer', return_value=MagicMock()) as mock_username_timer:
            event = MagicMock()
            self.window.close_event(event)
            mock_password_timer().stop.assert_called_once()
            mock_username_timer().stop.assert_called_once()
            event.accept.assert_called_once()

if __name__ == '__main__':
    unittest.main()