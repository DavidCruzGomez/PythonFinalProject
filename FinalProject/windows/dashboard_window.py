# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication

class DashboardWindow(QMainWindow):
    """
    Dashboard window class.

    This class represents the main dashboard that users see after logging in.
    """

    def __init__(self) -> None:
        """
        Initialize the dashboard window.
        """
        super().__init__()

        # Set the dashboard window's properties
        self.setWindowTitle("Final project David Cruz Gómez")

        # Get the screen size using QScreen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()

        # Set the window size as a relative value
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)

        # Calculate the position to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Adjust for system taskbars or other offsets
        x_position = max(0, x_position)  # Ensure it doesn't go outside the screen
        y_position = max(0, y_position)  # Ensure it doesn't go outside the screen

        # Set the geometry with the calculated position
        self.setGeometry(x_position, y_position, window_width, window_height)

        # Create a layout for the dashboard content
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a welcome label
        welcome_label = QLabel("Welcome to the Dashboard!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Set the layout to a central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
