# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

# Local project-specific imports
from src.assets.users_db import add_user_to_db
from src.assets.utils import show_message, PasswordValidator, UsernameValidator
from src.assets.custom_errors import InputValidationError, WidgetError
from src.styles.styles import create_title, create_input_field, create_button


class RegistrationWindow(QWidget):
    """
    User Registration Window.

    This class handles the user registration UI, including real-time validation
    of the username and password fields, and user registration in the database.

    Attributes:
        username_input (QLineEdit): Input field for the username.
        email_input (QLineEdit): Input field for the email address.
        password_input (QLineEdit): Input field for the password.
        password_validator (PasswordValidator): Validator for the password.
        username_validator (UsernameValidator): Validator for the username.
        register_button (QPushButton): Button for user registration.
        _is_closing (bool): Flag to track if the window is closing.
        _is_registered (bool): Flag to track if the user has successfully registered.
    """
    def __init__(self) -> None:
        """
        Initializes the user registration window.

        Sets up the UI, including input fields, buttons, and validators for
        the username and password. It also connects the text fields to their
        respective validation functions.

        Calls validation methods to provide real-time feedback as the user types
        in the input fields.
        """
        super().__init__()
        self.setWindowTitle("User Registration")
        self.setGeometry(100, 100, 400, 300)

        # Create layout and center widgets
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Use the `create_title` function from styles.py
        layout.addWidget(create_title("User Registration"))

        # Input fields
        self.username_input = create_input_field("Username")
        self.email_input = create_input_field("Email")
        self.password_input = create_input_field("Password", is_password=True)

        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)

        # Initialize PasswordValidator
        self.password_validator = PasswordValidator()

        # Add password labels to the layout
        for label in self.password_validator.create_labels():
            layout.addWidget(label)

        # Initialize UsernameValidator
        self.username_validator = UsernameValidator()

        # Add username labels to the layout
        for label in self.username_validator.create_labels():
            layout.addWidget(label)

        # Connect input fields to validation functions
        self.username_input.textChanged.connect(self._validate_username)
        self.password_input.textChanged.connect(self._validate_password)

        # Create register button using the `create_button` function from styles.py
        self.register_button = create_button("Register", self._on_register)
        layout.addWidget(self.register_button)

        # Set layout
        self.setLayout(layout)

        # Flag to track if window is closing
        self._is_closing: bool = False
        self._is_registered: bool = False

        print("📝 [INFO] Registration Window Initialized.")


    def close_event(self, event):
        """
        Handles the window close event.

        Stops the validation timers when the registration window is closed,
        ensuring that validation does not continue in the background. Also ensures
        that no further validation occurs if the window is closing or if the
        registration has already been completed.

        Args:
            event (QClose_event): The close event of the window.
        """
        self._is_closing = True  # Mark that the window is closing

        if not self._is_registered:
            print("⚠️ [WARNING] Closing registration window, stopping validation.")

        try:
            self.password_validator.get_timer().stop()  # Stop the password validation timer
            self.username_validator.get_timer().stop()  # Stop the username validation timer

        except AttributeError as att_err:
            # Handle missing get_timer() or uninitialized password_validator
            print(f"❌ [ERROR] Failed to access timer or validator: {att_err}")
            raise InputValidationError(f"Failed to stop validation timers: {att_err}") from att_err

        except Exception as gen_err:
            print("❌ [ERROR] An unexpected error occurred while"
                  f" stopping validation timers: {gen_err}")
            raise InputValidationError("Unexpected error while stopping timers:"
                                       f" {gen_err}") from gen_err
        event.accept()


    def _validate_password(self) -> None:
        """
        Validates the password in real-time as the user types.

        Displays password requirements and validates that the password meets
        security criteria. If the password does not meet the requirements, it shows
        the corresponding error labels.

        It also restarts the timer to hide the error labels after a period of inactivity.

        Only validates if the window is not closing and if the registration is not successful.
        """
        if self._is_closing or  self._is_registered:  # Do not validate if the window is closing or
            # the registration is successful
            return

        password: str = self.password_input.text().strip()

        # Show and validate password requirements
        self.password_validator.show_labels()
        self.password_validator.validate_password(password)

        # Restart the timer to hide labels after inactivity
        timer = self.password_validator.get_timer()

        if timer:
            timer.start()
        else:
            raise WidgetError("Failed to retrieve the password validation timer.")


    def _validate_username(self) -> None:
        """
        Validates the username in real-time as the user types.

        Displays username requirements and validates that the username meets
        the necessary criteria. If the username is invalid, it shows the corresponding
        error labels.

        It also restarts the timer to hide the error labels after a period of inactivity.

        Only validates if the window is not closing and if the registration is not successful.
        """
        if self._is_closing or self._is_registered:  # Do not validate if the window is closing or
            # the registration is successful
            return

        username: str = self.username_input.text().strip()

        # Show and validate username requirements
        self.username_validator.show_labels()
        self.username_validator.validate_username(username)

        # Restart the timer to hide labels after inactivity
        timer = self.username_validator.get_timer()

        if timer:
            timer.start()
        else:
            raise WidgetError("Failed to retrieve the username validation timer.")


    def _on_register(self) -> None:
        """
        Handles user registration, including password hashing.

        Validates the input fields (username, email, and password), and if all are valid,
        attempts to register the user in the database. If registration is successful, it shows
        a success message and closes the window.

        If an error occurs during registration, an appropriate error message is shown.

        It also clears input fields and hides validation labels after successful registration.

        Raises:
            ValueError: If user registration fails (e.g., due to database issues).
        """
        username: str = self.username_input.text().strip()
        email: str = self.email_input.text().strip()
        password: str = self.password_input.text().strip()

        # Validate empty fields
        if not username or not email or not password:
            show_message(self, "Error", "Please fill in all fields.")
            print("❌ [ERROR] Registration failed: One or more fields are empty.")
            return

        # Validate username
        if not self.username_validator.validate_username(username):
            show_message(self, "Error", "Username does not meet all requirements.")
            print("❌ [ERROR] Registration failed: Invalid username.")
            return

        # Validate password
        if not self.password_validator.validate_password(password):
            show_message(self, "Error", "Password does not meet all requirements.")
            print("❌ [ERROR] Registration failed: Invalid password.")
            return

        # Attempt to register the user in the database
        try:
            add_user_to_db(username, email, password)
            show_message(self, "Success", f"User {username} registered successfully!")

            # Mark as successfully registered
            self._is_registered = True

            # Clear input fields after successful registration
            self.username_input.clear()
            self.email_input.clear()
            self.password_input.clear()

            # Hide validation labels after successful registration
            for label in self.password_validator.get_labels():
                label.hide()
            for label in self.username_validator.get_labels():
                label.hide()

            # Close the registration window
            self.close()
            print("📝 [INFO] Registration window closed.")

        except ValueError as value_err:
            show_message(self, "Error", str(value_err))  # Show error message to the user
            print(f"❌ [ERROR] Registration failed: {str(value_err)}")
