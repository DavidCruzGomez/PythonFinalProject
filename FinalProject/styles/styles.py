# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton
from FinalProject.assets.custom_errors import WidgetError, InputValidationError


# Styles for widgets
STYLES = {
    "button": """
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
    """,

    "main_window": """
        QMainWindow {
            background-color: #F5F5F5;
        }
    """,

    "text_field": """
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
    """,

    "feedback": {
        "success": "color: green; font-size: 16px;",
        "error": "color: red; font-size: 16px;",
        "info": "color: blue; font-size: 16px;",
    },

    "title": "font-size: 30px; color: #333;",

    "password_recovery_link": """
        QLabel {
            color: #1A91DA;
            font-size: 16px;
            text-decoration: none;
        }
        QLabel:hover {
            text-decoration: underline;
        }
    """,

    "scroll_area": """
        QScrollArea {
            background-color: white;
            border: 4px solid #8ED0F8;
            border-radius: 10px;
            max-width: 800px;
            max-height: 206px;
        }
    
        QTableWidget {
            width: 100%;
            border: 1px solid #8ED0F8; /* Light borders around the table */
            border-radius: 5px; /* Rounded corners */
            background-color: #f9f9f9; /* Light background color */
            gridline-color: #8ED0F8;
        }
    
        QTableWidget::item {
            padding: 8px;
            font-size: 16px;
            background-color: white;
            border-right: 1px solid #e1e1e1; /* Separators between columns */
            border-bottom: 1px solid #e1e1e1; /* Separators between rows */
        }
    
        QTableWidget::item:selected {
            background-color: #8ED0F8; /* Color when a cell is selected */
            color: white;
        }
    
        QHeaderView::section {
            background-color: #1A91DA; /* Header background */
            color: white;
            font-size: 18px;
            padding: 5px;
        }
    
        QTableWidget QTableCornerButton::section {
            background-color: transparent; /* No background color for corners */
        }
    
        /* Customization of vertical scrollbar */
        QScrollBar:vertical {
            background: #f2f2f2;
            width: 12px;
            border-radius: 6px;
        }
    
        QScrollBar::handle:vertical {
            background: #8ED0F8;
            border-radius: 6px;
            min-height: 30px;
        }
    
        QScrollBar::handle:vertical:hover {
            background: #1A91DA;
        }
    
        QScrollBar::add-line:vertical {
            border: none;
            background: #f2f2f2;
            height: 0px;
        }
    
        QScrollBar::sub-line:vertical {
            border: none;
            background: #f2f2f2;
            height: 0px;
        }
    
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            border: none;
            background: none;
        }
    
        /* Customization of horizontal scrollbar */
        QScrollBar:horizontal {
            background: #f2f2f2;
            height: 12px;
            border-radius: 6px;
        }
    
        QScrollBar::handle:horizontal {
            background: #8ED0F8;
            border-radius: 6px;
            min-width: 30px;
        }
    
        QScrollBar::handle:horizontal:hover {
            background: #1A91DA;
        }
    
        QScrollBar::add-line:horizontal {
            border: none;
            background: #f2f2f2;
            width: 0px;
        }
    
        QScrollBar::sub-line:horizontal {
            border: none;
            background: #f2f2f2;
            width: 0px;
        }
    
        QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
            border: none;
            background: none;
        }
    """,

    "menu_bar": """
        QMenuBar {
            background-color: #8ED0F8;
            border: none;
            font-size: 18px;
            color: #333333; /* Color del texto */
        }

        QMenuBar::item {
            background-color: transparent; /* Transparent background by default */
            padding: 8px 15px;
        }

        QMenuBar::item:selected {
            background-color: #1A91DA; /* Light blue background when an item is selected */
            color: white; /* White text when selected */
        }

        QMenuBar::item:hover {
            background-color: #1A91DA; /* Darker blue background when hovered */
            color: white; /* White text when hovered */
        }

        QMenu {
            background-color: #FFFFFF; /* White background for the menus */
            border: 1px solid #8ED0F8; /* Light blue border */
            border-radius: 5px; /* Rounded corners */
        }

        QMenu::item {
            background-color: transparent; /* Transparent background for menu items */
            padding: 8px 20px;
            color: #333333; /* Color del texto */
        }

        QMenu::item:selected {
            background-color: #8ED0F8; /* Light blue background when a menu item is selected */
            color: white; /* White text when selected */
        }

        QMenu::item:hover {
            background-color: #1A91DA; /* Darker blue background when hovered */
            color: white; /* White text when hovered */
        }
    """,

    "menu_button": """
        QPushButton {
            background-color: #1A91DA; /* Blue to match the menu */
            color: white;
            border: none;
            font-size: 20px;
            padding: 10px 20px;
            min-width: 150px;
        }
        QPushButton:hover {
            background-color: #8ED0F8; /* Change to light blue when hovered */
        }
        QPushButton:pressed {
            background-color: #1A91DA; /* Maintain the color when pressed */
            opacity: 0.8; /* Visual effect when pressed */
        }
    """,

    "toggle_button": """
        QPushButton {
            background-color: #8ED0F8;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            padding: 5px;
            min-width: 120px;
            qproperty-cursor: "PointingHandCursor";
        }
        QPushButton:hover {
            background-color: #1A91DA;
        }
    """,

    "combo_box": """
        /* Main style for QComboBox */
        QComboBox {
            background-color: white;
            border: 2px solid #8ED0F8;
            border-radius: 10px;
            font-size: 18px;
            padding: 10px;
            min-width: 500px;
            color: #333333;
        }
    
        /* Style for editable QComboBox */
        QComboBox:editable {
            background-color: white;
        }
        
        /* Style when QComboBox is focused (when clicked) */
        QComboBox:focus {
            border-color: #1A91DA;
        }
    
        /* Style for the dropdown button inside QComboBox */
        QComboBox::drop-down {
            border-left: 1px solid #8ED0F8;
            background-color: white;
            width: 25px;
        }
    
        /* Customization of the down arrow in QComboBox */
        QComboBox::down-arrow {
            width: 15px; /* Arrow size */
            height: 15px;
        }
    
        /* Style for the list that appears when QComboBox is opened */
        QComboBox QAbstractItemView {
            background-color: white;
            border: 1px solid #8ED0F8;
            selection-background-color: #8ED0F8;
            selection-color: white;
            font-size: 18px;
        }
    
        /* Style for the items inside the QComboBox list */
        QComboBox QAbstractItemView::item {
            padding: 8px;
        }
    
        QComboBox QAbstractItemView::item:selected {
            background-color: #1A91DA;
        }
    
        /* Style for the vertical scrollbar */
        QComboBox QAbstractItemView QScrollBar:vertical {
            background: #f2f2f2;
            width: 12px;
            border-radius: 6px;
        }
    
        /* Style for the "handle" or control of the vertical scrollbar */
        QComboBox QAbstractItemView QScrollBar::handle:vertical {
            background: #8ED0F8;
            border-radius: 6px;
            min-height: 30px;
        }
    
        QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {
            background: #1A91DA;
        }
    
        /* Style for the additional lines at the top and bottom of the scrollbar */
        QComboBox QAbstractItemView QScrollBar::add-line:vertical {
            border: none;
            background: #f2f2f2;
            height: 0px;
        }
    
        QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
            border: none;
            background: #f2f2f2;
            height: 0px;
        }
    
        /* Style of the arrows of the vertical scrollbar */
        QComboBox QAbstractItemView QScrollBar::up-arrow:vertical, 
        QComboBox QAbstractItemView QScrollBar::down-arrow:vertical {
            border: none;
            background: none;
        }
    """
}

# Constants for input fields and button sizes
DEFAULT_INPUT_WIDTH = 500
DEFAULT_INPUT_HEIGHT = 50
DEFAULT_BUTTON_WIDTH = 200
DEFAULT_BUTTON_HEIGHT = 50


def create_title(title_text: str) -> QLabel:
    """
    Creates and returns a QLabel to display the title with the defined style.

    Args:
        title_text (str): The text to display on the title label.

    Returns:
        QLabel: A QLabel widget with the title and applied style.

    Raises:
        WidgetError: If there is an issue creating the label.
    """
    try:
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(STYLES["title"])
        return title

    except InputValidationError as in_val_err:
        print(f"❌ [ERROR] {in_val_err}")
        raise

    except Exception as gen_err:
        print(f"❌ [ERROR] Failed to create title label: {gen_err}")
        raise WidgetError(f"Failed to create title label: {gen_err}") from gen_err


def create_input_field(placeholder: str, is_password: bool = False,
                       width: int = DEFAULT_INPUT_WIDTH, height: int = DEFAULT_INPUT_HEIGHT
                      ) -> QLineEdit:
    """
    Creates and returns a styled text input field.

    Args:
        placeholder (str): The placeholder text to display in the input field.
        is_password (bool): If True, the text will be hidden (for password input).
        width (int): The width of the input field.
        height (int): The height of the input field.

    Returns:
        QLineEdit: A QLineEdit widget with the specified style.

    Raises:
        WidgetError: If there is an issue creating the input field.
    """
    try:
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        if is_password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
        input_field.setStyleSheet(STYLES["text_field"])
        input_field.setFixedSize(width, height)
        return input_field

    except InputValidationError as in_val_err:
        print(f"❌ [ERROR] {in_val_err}")
        raise

    except Exception as gen_err:
        print(f"❌ [ERROR] Failed to create input field: {gen_err}")
        raise WidgetError(f"Failed to create input field with placeholder "
                          f"'{placeholder}': {gen_err}") from gen_err


def create_button(button_text: str, callback: callable, width: int = DEFAULT_BUTTON_WIDTH,
                  height: int = DEFAULT_BUTTON_HEIGHT) -> QPushButton:
    """
    Creates and returns a QPushButton with custom text, style, and size.

    Args:
        button_text (str): The text to display on the button.
        callback (callable): The function to be executed when the button is clicked.
        width (int): The width of the button.
        height (int): The height of the button.

    Returns:
        QPushButton: A QPushButton widget with the specified text and style.

    Raises:
        WidgetError: If there is an issue creating the button.
    """
    try:
        button = QPushButton(button_text)
        button.setFixedSize(width, height)
        button.setStyleSheet(STYLES["button"])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        return button

    except Exception as gen_err:
        print(f"❌ [ERROR] Failed to create button with text '{button_text}': {gen_err}")
        raise WidgetError(f"Failed to create button with text '{button_text}': {gen_err}")\
            from gen_err


def style_feedback_label(label: QLabel, message: str, message_type: str = "info") -> None:
    """
    Updates and styles the feedback label with the specified message and style.

    Args:
        label (QLabel): The label to update with the message.
        message (str): The message to display in the label.
        message_type (str): The type of message ("success", "error", or "info").

    Raises:
        InputValidationError: If the message type is invalid.
    """

    if message_type not in STYLES["feedback"]:
        raise InputValidationError(f"Invalid message type: {message_type}")

    try:
        label.setText(message)
        label.setStyleSheet(STYLES["feedback"].get(message_type, STYLES["feedback"]["info"]))

    except InputValidationError as in_val_err:
        print(f"❌ [ERROR] {in_val_err}")
        label.setText("Error: Invalid message type.")
        label.setStyleSheet(STYLES["feedback"]["error"])

    except Exception as gen_err:
        print(f"❌ [ERROR] An error occurred while styling feedback label: {gen_err}")
        label.setText("An unexpected error occurred.")
        label.setStyleSheet(STYLES["feedback"]["error"])
