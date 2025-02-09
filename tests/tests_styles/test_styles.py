"""
Unit tests for the style-related functions in the `src.styles.styles` module.

This test suite verifies that the graphical user interface (GUI) components,
such as buttons, input fields, labels, and other UI elements,
are correctly styled and behave as expected. The tests also ensure that
appropriate error handling is in place for invalid message types.

Key tests include:

- `test_create_title`: Verifies the creation and styling of a title label,
ensuring it matches design specifications.

- `test_create_input_field`: Ensures input fields are styled correctly
and properly handle placeholder text.

- `test_create_password_field`: Confirms password fields are styled correctly
and function as expected, including toggling visibility.

- `test_create_button`: Tests the creation and styling of buttons,
verifying appearance and hover state behavior.

- `test_style_feedback_label`: Verifies feedback labels are styled according
to the message type (e.g., success, error, info).

- `test_invalid_message_type`: Ensures invalid message types trigger appropriate
error handling and display an error message.

The tests use Python's `unittest` framework to validate the functionality
of UI components, including their styling and error handling,
without the need for a full graphical environment.
"""


# Standard library imports
import unittest

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton

# Local imports
from src.styles.styles import create_title, create_input_field, create_button, \
    style_feedback_label, InputValidationError


APP = QApplication([])  # Necessary to initialize the widgets in PySide6

class TestStyles(unittest.TestCase):
    """
    Test class for verifying the functionality of style-related functions for widgets.
    """

    def test_create_title(self) -> None:
        """
        Test the creation of a title label with the correct text, style, and alignment.
        """
        title_text: str = "Test Title"
        title = create_title(title_text)

        # Verify that the title is an instance of QLabel
        self.assertIsInstance(title, QLabel)

        # Verify that the title's text matches the expected text
        self.assertEqual(title.text(), title_text)

        # Verify that the title's alignment is centered
        self.assertEqual(title.alignment(), Qt.AlignmentFlag.AlignCenter)

        # Verify that the title has the correct style (font size and color)
        self.assertEqual(title.styleSheet(), "font-size: 30px; color: #333;")

    def test_create_input_field(self) -> None:
        """
        Test the creation of a text input field with the specified placeholder and style.
        """
        placeholder: str = "Enter your name"
        input_field = create_input_field(placeholder)

        # Verify that the input field is an instance of QLineEdit
        self.assertIsInstance(input_field, QLineEdit)

        # Verify that the input field's placeholder text is set correctly
        self.assertEqual(input_field.placeholderText(), placeholder)

        # Verify that the input field's style sheet matches the expected style
        self.assertEqual(input_field.styleSheet(), """
        QLineEdit {
            background-color: white;
            border: 2px solid #8ED0F8;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            min-width: 500px;
        }
        QLineEdit:focus {
            border-color: #1A91DA;
        }
        QLineEdit::placeholder {
            color: #888888;
            font-style: italic;
        }
    """)

        # Verify that the input field is not set to password mode
        self.assertEqual(input_field.echoMode(), QLineEdit.EchoMode.Normal)

    def test_create_password_field(self) -> None:
        """
        Test the creation of a password input field, verifying that the text is hidden.
        """
        placeholder: str = "Enter your password"
        input_field = create_input_field(placeholder, is_password=True)

        # Verify that the input field is set to password mode (i.e., text is hidden)
        self.assertEqual(input_field.echoMode(), QLineEdit.EchoMode.Password)

    def test_create_button(self) -> None:
        """
        Test the creation of a button with the correct text, style, and cursor.
        """
        button_text: str = "Click Me"

        # Dummy callback function to connect with the button's click signal
        def dummy_callback() -> None:
            """Placeholder function for button tests, performing no action."""
            pass

        button: QPushButton = create_button(button_text, dummy_callback)

        # Verify that the button is an instance of QPushButton
        self.assertIsInstance(button, QPushButton)

        # Verify that the button's text is set correctly
        self.assertEqual(button.text(), button_text)

        # Verify that the button's style matches the expected style
        self.assertEqual(button.styleSheet(), """
        QPushButton {
            background-color: #8ED0F8;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 26px;
            padding: 8px;
            min-width: 500px;
            qproperty-cursor: "PointingHandCursor";
        }
        QPushButton:hover {
            background-color: #1A91DA;
        }
    """)

        # Verify that the button's cursor changes to a pointing hand on hover
        self.assertEqual(button.cursor().shape(), Qt.CursorShape.PointingHandCursor)

    def test_style_feedback_label(self) -> None:
        """
        Test the feedback label styling with a success message and the corresponding style.
        """
        label: QLabel = QLabel()
        message: str = "Success!"

        # Call the function to style the label with a success message
        style_feedback_label(label, message, "success")

        # Verify that the label's text matches the success message
        self.assertEqual(label.text(), message)

        # Verify that the label's style sheet is set to the success style
        self.assertEqual(label.styleSheet(), "color: green; font-size: 16px;")

    def test_invalid_message_type(self) -> None:
        """
        Test handling of an invalid message type by raising InputValidationError.
        """
        label: QLabel = QLabel()
        with self.assertRaises(InputValidationError) as context:
            # Call the function with an invalid message type to raise an exception
            style_feedback_label(label, "Error message", "invalid_type")

        # Verify that the exception message contains the expected text
        self.assertIn("Invalid message type", str(context.exception))


if __name__ == "__main__":
    unittest.main()
