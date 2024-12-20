# Standard library imports
import re

# Third-party imports
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QLabel

# Local imports
from FinalProject.assets.regex import password_regex, username_regex


def show_message(parent, title: str, message: str) -> None:
    """
    Displays a message in a message box.

    Args:
        parent: The parent widget (e.g., the main window).
        title (str): The title of the message.
        message (str): The message to be displayed in the message box.
    """
    try:
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
        print(f"📢 [INFO] Displayed message box: {title} - {message}")
    except Exception as e:
        print(f"❌ [ERROR] Failed to display message box. Error: {e}")

class ValidatorBase:
    """
    Base class for validators (e.g., PasswordValidator, UsernameValidator).
    Handles shared functionality like label creation and visibility management.
    """
    def __init__(self, requirements: list[str], timer_interval=2000):
        self.labels = []
        self.timer = QTimer()
        self.timer.setInterval(timer_interval)  # Hide labels after inactivity
        self.timer.timeout.connect(self.hide_labels)
        self.requirements = requirements  # List of requirement descriptions
        self.validation_state = [False] * len(requirements)  # Store validation state for each requirement
        print(f"🔄 [INFO] Validator initialized with {len(requirements)} requirements.")

    def create_labels(self) -> list[QLabel]:
        """
        Creates and returns requirement labels.
        """
        try:
            if not self.labels:
                self.labels = [QLabel(text) for text in self.requirements]
                for label in self.labels:
                    label.setStyleSheet("color: red;")
                    label.hide()  # Initially hide all labels
                print(f"✅ [SUCCESS] Created {len(self.labels)} requirement labels.")

            else:
                print("⚠️ [WARNING] Labels already created. Skipping creation.")
            return self.labels

        except Exception as e:
            print(f"❌ [ERROR] Failed to create labels for requirements. Error: {e}")
            return []

    def show_labels(self) -> None:
        """
        Shows all labels.
        """
        try:
            for label in self.labels:
                label.show()
        except Exception as e:
            print(f"❌ [ERROR] Failed to show labels. Error: {e}")

    def hide_labels(self) -> None:
        """
        Hides all labels and stops the timer.
        """
        try:
            for label in self.labels:
                label.hide()
            self.timer.stop()
        except Exception as e:
            print(f"❌ [ERROR] Failed to hide labels. Error: {e}")

    @staticmethod
    def validate_input(input_text: str, regex_list: list[tuple[str, QLabel]], validation_status: list[bool]) -> bool:
        """
        Validates the input using provided regex rules and updates label styles.

        Args:
            input_text (str): The input text to validate.
            regex_list (list[tuple[str, QLabel]]): A list of tuples containing regex patterns and corresponding labels.
            validation_status (list[bool]): The status of validation for each requirement.

        Returns:
            bool: True if all requirements are met, otherwise False.
        """
        try:
            all_requirements_met = True
            for index, (regex, label) in enumerate(regex_list):
                is_valid = bool(re.search(regex, input_text))

                if is_valid and not validation_status[index]:
                    label.setStyleSheet("color: green;")
                    print(f"✅ [SUCCESS] Requirement met: {label.text()}")

                elif not is_valid and validation_status[index]:
                    label.setStyleSheet("color: red;")
                    print(f"❌ [ERROR] Requirement not met: {label.text()}")

                validation_status[index] = is_valid  # Update validation status for this requirement
                all_requirements_met &= is_valid  # If any requirement is not met, set all_requirements_met to False
            return all_requirements_met

        except re.error as regex_error:
            print(f"❌ [ERROR] Regular expression error during input validation: {regex_error}")
            return False
        except Exception as e:
            print(f"❌ [ERROR] Unexpected error during input validation: {e}")
            return False


class PasswordValidator(ValidatorBase):
    """
    Specific validator for passwords, inherits from ValidatorBase.
    Validates a password in real-time.
    """
    def __init__(self):
        super().__init__([
            "At least one uppercase letter (A-Z).",
            "At least one lowercase letter (a-z).",
            "At least one number (0-9).",
            "At least one special character (@$!%*?&).",
            "At least 8 characters."
        ])
        self.validation_started = False
        print("🔄 [INFO] PasswordValidator initialized.")

    def validate_password(self, password: str) -> bool:
        """
        Validates the password and updates label styles in real-time.
        Returns True if all requirements are met, otherwise False.
        """
        try:
            if not self.validation_started:
                print("🔍 [INFO] Starting password validation.")
                self.validation_started = True

            requirements = [
                (password_regex['upper'], self.labels[0]),
                (password_regex['lower'], self.labels[1]),
                (password_regex['number'], self.labels[2]),
                (password_regex['special'], self.labels[3]),
                (password_regex['length'], self.labels[4]),
            ]
            return self.validate_input(password, requirements, self.validation_state)

        except Exception as e:
            print(f"❌ [ERROR] Unexpected error during password validation. Error: {e}")
            return False


class UsernameValidator(ValidatorBase):
    """
    Specific validator for usernames, inherits from ValidatorBase.
    Validates a username in real-time.
    """
    def __init__(self):
        super().__init__([
            "Length between 3 and 18 characters.",
            "Only alphanumeric characters, dots, hyphens, and underscores.",
            "Starts with alphanumeric.",
            "Ends with alphanumeric."
        ])
        self.validation_started = False
        print("🔄 [INFO] UsernameValidator initialized.")

    def validate_username(self, username: str) -> bool:
        """
        Validates the username using `username_regex` and updates label styles in real-time.
        Returns True if all requirements are met, otherwise False.
        """
        try:
            if not self.validation_started:
                print("🔍 [INFO] Starting username validation.")
                self.validation_started = True

            requirements = [
                (username_regex['length'], self.labels[0]),         # Validate length
                (username_regex['valid_chars'], self.labels[1]),    # Validate valid characters
                (username_regex['start_alnum'], self.labels[2]),    # Validate start with alphanumeric
                (username_regex['end_alnum'], self.labels[3]),      # Validate end with alphanumeric
            ]
            return self.validate_input(username, requirements, self.validation_state)

        except Exception as e:
            print(f"❌ [ERROR] Unexpected error during username validation. Error: {e}")
            return False