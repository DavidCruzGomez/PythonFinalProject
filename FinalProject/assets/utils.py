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

    Raises:
        Exception: If an error occurs while displaying the message box.
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

    Attributes:
        labels (list[QLabel]): List of QLabel objects to display validation requirements.
        timer (QTimer): Timer used to hide labels after a period of inactivity.
        requirements (list[str]): List of requirement descriptions for validation.
        validation_state (list[bool]): List to store the validation status of each requirement.

    Methods:
        create_labels(): Creates and returns requirement labels.
        show_labels(): Displays all requirement labels.
        hide_labels(): Hides all requirement labels and stops the timer.
        validate_input(input_text, regex_list, validation_status): Validates the input based on regex rules.
    """
    def __init__(self, requirements: list[str], timer_interval=2000):
        """
        Initializes the validator with given requirements and timer interval.

        Args:
            requirements (list[str]): List of validation requirements.
            timer_interval (int): Interval in milliseconds to hide labels after inactivity.
                Defaults to 2000ms.
        """
        self.labels = []
        self.timer = QTimer()
        self.timer.setInterval(timer_interval)  # Hide labels after inactivity
        self.timer.timeout.connect(self.hide_labels)
        self.requirements = requirements  # List of requirement descriptions
        self.validation_state = [False] * len(requirements)  # Store validation state for each requirement
        print(f"🔄 [INFO] Validator initialized with {len(requirements)} requirements.")

    def create_labels(self) -> list[QLabel]:
        """
        Creates and returns requirement labels for validation.

        Returns:
            list[QLabel]: List of QLabel objects created for the validation requirements.

        Raises:
            Exception: If there is an error creating the labels.
        """
        if not self.labels:
            try:
                # Create labels for each requirement and set initial style
                self.labels = [QLabel(req) for req in self.requirements]
                for label in self.labels:
                    label.setStyleSheet("color: red;")
                    label.hide()  # Initially hide all labels
                print(f"✅ [SUCCESS] Created {len(self.labels)} requirement labels.")
            except Exception as e:
                print(f"❌ [ERROR] Failed to create labels for requirements. Error: {e}")
                return []
        else:
            print("⚠️ [WARNING] Labels already created. Skipping creation.")

        return self.labels

    def show_labels(self) -> None:
        """
        Displays all validation labels.

        Raises:
            Exception: If there is an error displaying the labels.
        """
        try:
            for label in self.labels:
                label.show()
        except Exception as e:
            print(f"❌ [ERROR] Failed to show labels. Error: {e}")

    def hide_labels(self) -> None:
        """
        Hides all validation labels and stops the timer.

        Raises:
            Exception: If there is an error hiding the labels or stopping the timer.
        """
        try:
            for label in self.labels:
                label.hide()
            self.timer.stop()
        except Exception as e:
            print(f"❌ [ERROR] Failed to hide labels. Error: {e}")

    @staticmethod
    def validate_input(input_text: str, regex_list: list[tuple[str, QLabel]],
                       validation_status: list[bool]) -> bool:
        """
        Validates the input using provided regex rules and updates label styles.

        Args:
            input_text (str): The input text to validate.
            regex_list (list[tuple[str, QLabel]]): A list of tuples containing regex patterns and
                corresponding QLabel objects.
            validation_status (list[bool]): A list of validation statuses, updated for each requirement.

        Returns:
            bool: True if all validation requirements are met, otherwise False.

        Raises:
            re.error: If there is a regular expression error.
            Exception: If an unexpected error occurs during validation.
        """
        try:
            all_requirements_met = True
            for index, (regex, label) in enumerate(regex_list):
                is_valid = bool(re.search(regex, input_text))
                validation_status[index] = is_valid # Update the validation status for this requirement
                label.setStyleSheet("color: green;" if is_valid else "color: red;")
                all_requirements_met &= is_valid
                print(f"{'✅ [SUCCESS]' if is_valid else '❌ [ERROR]'} Requirement: {label.text()}")
            return all_requirements_met

        except re.error as regex_error:
            print(f"❌ [ERROR] Regular expression error during input validation: {regex_error}")
            return False
        except Exception as e:
            print(f"❌ [ERROR] Unexpected error during input validation: {e}")
            return False


class PasswordValidator(ValidatorBase):
    """
    Validator for passwords, inheriting from ValidatorBase.
    Validates password in real-time to ensure it meets specified requirements.

    Methods:
        validate_password(password: str): Validates the password using regex patterns and
            updates label styles.
    """
    def __init__(self):
        """
        Initializes the password validator with predefined password requirements.

        Inherits from ValidatorBase and sets up specific validation rules for passwords.
        """
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

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if all password requirements are met, otherwise False.

        Raises:
            Exception: If an error occurs during password validation.
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
    Validator for usernames, inheriting from ValidatorBase.
    Validates username in real-time to ensure it meets specified requirements.

    Methods:
        validate_username(username: str): Validates the username using regex patterns and
            updates label styles.
    """
    def __init__(self):
        """
        Initializes the username validator with predefined username requirements.

        Inherits from ValidatorBase and sets up specific validation rules for usernames.
        """
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
        Validates the username and updates label styles in real-time.

        Args:
            username (str): The username to validate.

        Returns:
            bool: True if all username requirements are met, otherwise False.

        Raises:
            Exception: If an error occurs during username validation.
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
