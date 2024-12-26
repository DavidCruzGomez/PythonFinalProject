# Standard library imports
import unittest
import json
import os


class TestEmailConfig(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        file_path = os.path.join(base_dir, 'FinalProject', 'assets', 'email_config.json')
        print(f"Attempting to open: {os.path.abspath(file_path)}")
        with open(file_path, 'r') as file:
            self.config = json.load(file)

    def test_sender_email(self):
        self.assertIn('sender_email', self.config)
        self.assertEqual(self.config['sender_email'], "noreply.impulsebuying@gmail.com")

    def test_sender_password(self):
        self.assertIn('sender_password', self.config)
        self.assertEqual(self.config['sender_password'], "kgoo jtms eplt njvj")

if __name__ == '__main__':
    unittest.main()
