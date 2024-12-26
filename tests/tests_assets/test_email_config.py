# Standard library imports
import unittest
import json
import os


class TestEmailConfig(unittest.TestCase):
    """
    Test suite for validating the email configuration file.

    This test class ensures that the 'email_config.json' file contains the required fields
    and that the values for the sender's email and password match the expected values.
    """

    def setUp(self):
        """
        Set up the test by loading the email configuration file.

        This method is called before every individual test. It attempts to open and load the
        'email_config.json' file into the `self.config` dictionary, making it accessible for
        the test methods.
        """
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        file_path = os.path.join(base_dir, 'FinalProject', 'assets', 'email_config.json')
        print(f"Attempting to open: {os.path.abspath(file_path)}")
        with open(file_path, 'r') as file:
            self.config = json.load(file)

    def test_sender_email(self):
        """
        Test that the sender's email is correctly defined in the configuration file.

        This test ensures that the 'sender_email' key exists in the configuration file and
        that its value is as expected.
        """
        self.assertIn('sender_email', self.config)
        self.assertEqual(self.config['sender_email'], "noreply.impulsebuying@gmail.com")

    def test_sender_password(self):
        """
        Test that the sender's password is correctly defined in the configuration file.

        This test ensures that the 'sender_password' key exists in the configuration file and
        that its value matches the expected encrypted password string.
        """
        self.assertIn('sender_password', self.config)
        self.assertEqual(self.config['sender_password'], "kgoo jtms eplt njvj")


if __name__ == '__main__':
    unittest.main()
