import unittest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication
from FinalProject.windows.main_window import MainWindow, WidgetError

class TestMainWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = MainWindow()

    def test_initial_state(self):
        self.assertEqual(self.window.windowTitle(), "Final project David Cruz Gómez")
        self.assertEqual(self.window._username_input.text(), "")
        self.assertEqual(self.window._password_input.text(), "")
        self.assertEqual(self.window._feedback_label.text(), "")

    @patch('FinalProject.windows.main_window.get_user_by_username')
    @patch('FinalProject.windows.main_window.get_user_by_email')
    @patch('FinalProject.windows.main_window.check_password_hash')
    def test_login_successful(self, mock_check_password_hash, mock_get_user_by_email, mock_get_user_by_username):
        self.window._username_input.setText("testuser")
        self.window._password_input.setText("testpassword")
        mock_get_user_by_username.return_value = {"password_hash": "hashed_password"}
        mock_check_password_hash.return_value = True

        with patch.object(self.window, '_login_successful') as mock_login_successful:
            self.window._on_login()
            mock_login_successful.assert_called_once()

    def test_empty_username(self):
        self.window._username_input.setText("")
        self.window._password_input.setText("testpassword")

        with patch.object(self.window._feedback_label, 'setText') as mock_set_text:
            self.window._on_login()
            mock_set_text.assert_called_with("Username cannot be empty.")

    def test_empty_password(self):
        self.window._username_input.setText("testuser")
        self.window._password_input.setText("")

        with patch.object(self.window._feedback_label, 'setText') as mock_set_text:
            self.window._on_login()
            mock_set_text.assert_called_with("Password cannot be empty.")

    def test_invalid_credentials(self):
        self.window._username_input.setText("testuser")
        self.window._password_input.setText("wrongpassword")

        with patch('FinalProject.windows.main_window.get_user_by_username', return_value=None):
            with patch.object(self.window._feedback_label, 'setText') as mock_set_text:
                self.window._on_login()
                mock_set_text.assert_called_with("User not found. Please try again.")

    @patch('FinalProject.windows.main_window.get_user_by_email')
    def test_handle_login_error_incorrect_password(self, mock_get_user_by_email):
        self.window._username_input.setText("testuser")
        self.window._password_input.setText("wrongpassword")
        mock_get_user_by_email.return_value = {"password_hash": "hashed_password"}

        with patch('FinalProject.windows.main_window.check_password_hash', return_value=False):
            with patch.object(self.window._feedback_label, 'setText') as mock_set_text:
                self.window._on_login()
                mock_set_text.assert_called_with("Incorrect password. Please try again.")

    @patch('FinalProject.windows.main_window.RegistrationWindow')
    def test_open_registration_window(self, MockRegistrationWindow):
        mock_window_instance = MockRegistrationWindow.return_value
        mock_window_instance.show = MagicMock()
        self.window._open_registration_window()
        mock_window_instance.show.assert_called_once()

    @patch('FinalProject.windows.main_window.RecoveryWindow')
    def test_open_recovery_window(self, MockRecoveryWindow):
        mock_window_instance = MockRecoveryWindow.return_value
        mock_window_instance.show = MagicMock()
        self.window._open_recovery_window()
        mock_window_instance.show.assert_called_once()


if __name__ == '__main__':
    unittest.main()
