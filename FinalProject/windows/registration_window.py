# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

# Local project-specific imports
from FinalProject.assets.users_db import add_user_to_db
from FinalProject.assets.utils import show_message, PasswordValidator, UsernameValidator
from FinalProject.styles.styles import create_title, create_input_field, create_button


class RegistrationWindow(QWidget):
    def __init__(self) -> None:
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
        self.username_input.textChanged.connect(self.validate_username)
        self.password_input.textChanged.connect(self.validate_password)

        # Create register button using the `create_button` function from styles.py
        self.register_button = create_button("Register", self.on_register)
        layout.addWidget(self.register_button)

        # Set layout
        self.setLayout(layout)

        # Flag to track if window is closing
        self.is_closing = False
        self.is_registered = False

        print("📝 [INFO] Registration Window Initialized.")

    def closeEvent(self, event):
        """
        Stop the timer and validation when the registration window is closed.
        """
        self.is_closing = True  # Mark that the window is closing
        if not self.is_registered:
            print("⚠️ [WARNING] Closing registration window, stopping validation.")
        self.password_validator.timer.stop()  # Stop the password validation timer
        self.username_validator.timer.stop()  # Stop the username validation timer
        event.accept()

    def validate_password(self) -> None:
        """
        Validates the password in real-time as the user types.
        Shows individual password requirements with visual feedback.
        """
        if self.is_closing or  self.is_registered:  # Do not validate if the window is closing or the registration is successful
            return

        password = self.password_input.text().strip()

        # Show and validate password requirements
        self.password_validator.show_labels()
        self.password_validator.validate_password(password)

        # Restart the timer to hide labels after inactivity
        self.password_validator.timer.start()


    def validate_username(self) -> None:
        """
        Validates the username in real-time as the user types.
        Provides feedback based on validity.
        """
        if self.is_closing or self.is_registered:  # Do not validate if the window is closing or the registration is successful
            return

        username = self.username_input.text().strip()

        # Show and validate username requirements
        self.username_validator.show_labels()
        self.username_validator.validate_username(username)

        # Restart the timer to hide labels after inactivity
        self.username_validator.timer.start()

    def on_register(self) -> None:
        """
        Handles user registration, including password hashing.
        """
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

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
            show_message( self,"Success", f"User {username} registered successfully!")

            # Mark as successfully registered
            self.is_registered = True

            # Clear input fields after successful registration
            self.username_input.clear()
            self.email_input.clear()
            self.password_input.clear()

            # Hide validation labels after successful registration
            for label in self.password_validator.labels:
                label.hide()
            for label in self.username_validator.labels:
                label.hide()

            # Close the registration window
            self.close()
            print("📝 [INFO] Registration window closed.")

        except ValueError as e:
            show_message(self, "Error", str(e))  # Show error message to the user
            print(f"❌ [ERROR] Registration failed: {str(e)}")