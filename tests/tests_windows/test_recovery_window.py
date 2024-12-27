import json
import smtplib
import unittest
from unittest.mock import patch, mock_open

from PySide6.QtWidgets import QApplication

from FinalProject.windows.recovery_window import RecoveryWindow, load_email_config, \
    EmailConfigError, EmailSender, EmailSendingError


class TestRecoveryWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])


    @patch('FinalProject.windows.recovery_window.EMAIL_CONFIG_FILE',
           'C:/Users/David/PycharmProjects/PythonProject1/FinalProject/assets/email_config.json')
    def setUp(self):
        self.window = RecoveryWindow()


    def test_initial_state(self):
        self.assertEqual(self.window.windowTitle(), "Password Recovery")
        self.assertEqual(self.window._email_input.text(), "")


    @patch('FinalProject.windows.recovery_window.show_message')
    @patch.object(EmailSender, 'send_recovery_email')
    @patch('FinalProject.windows.recovery_window.get_user_by_email')
    def test_recover_password_user_not_found(self, mock_get_user_by_email, mock_send_recovery_email,
                                             mock_show_message):
        mock_get_user_by_email.return_value = None
        self.window._email_input.setText("nonexistent@example.com")

        self.window._recover_password()

        mock_show_message.assert_called_with(self.window, "Error",
                                             "Email not found. Please try again.")
        self.assertEqual(self.window._email_input.text(), "")


    @patch('FinalProject.windows.recovery_window.get_user_by_email')
    @patch.object(EmailSender, 'send_recovery_email')
    @patch(
        'FinalProject.windows.recovery_window.show_message')  # Patch show_message where it is used
    def test_recover_password_success(self, mock_show_message, mock_send_recovery_email,
                                      mock_get_user_by_email):
        mock_get_user_by_email.return_value = {"name": "Test User"}
        self.window._email_input.setText("test@example.com")

        self.window._recover_password()

        # Assert send_recovery_email was called with the correct arguments
        mock_send_recovery_email.assert_called_with("test@example.com", "Test User")

        # Assert show_message was called with the correct arguments
        mock_show_message.assert_called_with(self.window, "Success",
                                             "A recovery email has been sent.")


    def test_load_email_config_success(self):
        fake_email_config = {
            "sender_email": "sender@example.com",
            "sender_password": "password"
        }

        with patch('os.path.exists', return_value=True), \
                patch('builtins.open', mock_open(read_data=json.dumps(fake_email_config))):
            # Call the actual function
            config = load_email_config()

            # Assertions
            self.assertEqual(config["sender_email"], "sender@example.com")
            self.assertEqual(config["sender_password"], "password")


    @patch('FinalProject.windows.recovery_window.load_email_config')
    def test_load_email_config_error(self, mock_load_email_config):
        mock_load_email_config.side_effect = EmailConfigError("Configuration error")

        with self.assertRaises(EmailConfigError):
            load_email_config()


    @patch('FinalProject.windows.recovery_window.smtplib.SMTP')
    def test_send_recovery_email_success(self, mock_smtp):
        email_sender = EmailSender(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            sender_email="sender@example.com",
            sender_password="password"
        )
        mock_server = mock_smtp.return_value.__enter__.return_value

        email_sender.send_recovery_email("recipient@example.com", "Test User")
        mock_server.sendmail.assert_called()


    @patch('FinalProject.windows.recovery_window.smtplib.SMTP')
    def test_send_recovery_email_failure(self, mock_smtp):
        email_sender = EmailSender(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            sender_email="sender@example.com",
            sender_password="password"
        )
        mock_smtp.side_effect = smtplib.SMTPException

        with self.assertRaises(EmailSendingError):
            email_sender.send_recovery_email("recipient@example.com", "Test User")


if __name__ == '__main__':
    unittest.main()
    