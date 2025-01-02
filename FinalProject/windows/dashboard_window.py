import os

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication,
                               QMenuBar, QMessageBox, QWidgetAction, QPushButton)
import subprocess
import sys

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

        # Create a menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Add a "File" menu
        file_menu = menu_bar.addMenu("File")

        # Create a custom widget action for the "Download XLSX" button
        download_action = QWidgetAction(self)

        # Create a custom QWidget (e.g., a button) to be added as an action
        download_button = QPushButton("Download XLSX")
        download_button.clicked.connect(self.download_xlsx)

        # Set the widget (the button) into the QWidgetAction
        download_action.setDefaultWidget(download_button)

        # Add the action (button) to the "File" menu
        file_menu.addAction(download_action)

    def download_xlsx(self):
        """Call the download_files.py script to download the latest XLSX file."""
        try:
            # Get the directory where the script is being executed
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Build the relative path to the 'download_files.py' script
            script_path = os.path.join(current_dir, "..", "assets", "download_files.py")

            # Run the script using the same Python executable that's running the application
            subprocess.run([sys.executable, script_path], check=True)

            # If the download is successful, display a message
            QMessageBox.information(self, "Download", "File downloaded successfully.")

        except subprocess.CalledProcessError as e:
            # If an error occurs during the script execution
            print(f"An error occurred while downloading the file: {e}")
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while downloading the file: {e}")

        except FileNotFoundError:
            print("File not found. Please check the path to the script.")
        except Exception as e:
            print(f"Unexpected error: {e}")