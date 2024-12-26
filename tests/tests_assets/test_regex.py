# Standard library imports
import unittest
import re

# Local imports
from FinalProject.assets.regex import EMAIL_REGEX, PASSWORD_REGEX, USERNAME_REGEX


class TestRegexPatterns(unittest.TestCase):
    def test_email_regex(self):
        valid_emails = [
            "test@example.com", "user.name@domain.co", "user_name@domain.com",
            "user-name@domain.io", "user+name@domain.com"
        ]
        invalid_emails = [
            "plainaddress", "@missingusername.com", "username@.com",
            "username@domain..com", "username@domain.c", "user@domain,com"
        ]
        for email in valid_emails:
            self.assertTrue(re.match(EMAIL_REGEX, email))
        for email in invalid_emails:
            self.assertFalse(re.match(EMAIL_REGEX, email))

    def test_password_regex(self):
        valid_passwords = [
            "Password1!", "Strong$Pass2", "Val1d@Pass"
        ]
        invalid_passwords = [
            "short1!", "noSpecialChar1", "NoNumber!", "12345678", "ALLUPPERCASE1!", "alllowercase1!"
        ]
        for password in valid_passwords:
            self.assertTrue(re.match(PASSWORD_REGEX['all'], password))
        for password in invalid_passwords:
            self.assertFalse(re.match(PASSWORD_REGEX['all'], password))

    def test_username_regex(self):
        valid_usernames = [
            "user123", "username", "user.name", "user-name", "user_name"
        ]
        invalid_usernames = [
            "us", "a" * 19, "user@name", ".username", "username.", "-username", "username-"
        ]
        for username in valid_usernames:
            self.assertTrue(re.match(USERNAME_REGEX['all'], username))
        for username in invalid_usernames:
            self.assertFalse(re.match(USERNAME_REGEX['all'], username))

if __name__ == '__main__':
    unittest.main()
