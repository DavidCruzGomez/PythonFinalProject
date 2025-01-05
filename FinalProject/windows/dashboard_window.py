import os
import subprocess
import sys

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication,
                               QMenuBar, QMessageBox, QWidgetAction, QPushButton,
                               QTableWidget, QTableWidgetItem, QScrollArea)
import pandas as pd
from FinalProject.styles.styles import STYLES

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
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

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
        welcome_label.setStyleSheet(STYLES["title"])
        layout.addWidget(welcome_label)

        # Create a scroll area to contain the table widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a table widget to display the XLSX data
        self.table_widget = QTableWidget()

        # Set the table widget as the widget for the scroll area
        scroll_area.setWidget(self.table_widget)

        # Add the scroll area to the layout
        layout.addWidget(scroll_area)

        # Set the scroll area style
        scroll_area.setStyleSheet(STYLES["scroll_area"])

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
        download_button.setStyleSheet(STYLES["menu_button"])

        download_button.clicked.connect(self.download_xlsx)

        # Set the widget (the button) into the QWidgetAction
        download_action.setDefaultWidget(download_button)

        # Add the action (button) to the "File" menu
        file_menu.addAction(download_action)

        # Create a custom widget action for the "Upload XLSX" button
        preprocess_action = QWidgetAction(self)

        # Create a custom QWidget (e.g., a button) to be added as an action
        preprocess_button = QPushButton("Preprocess XLSX")
        preprocess_button.setStyleSheet(STYLES["menu_button"])

        preprocess_button.clicked.connect(self.run_preprocessing)

        # Set the widget (the button) into the QWidgetAction
        preprocess_action.setDefaultWidget(preprocess_button)

        # Add the action (button) to the "File" menu
        file_menu.addAction(preprocess_action)

        # Set the style for the menu bar
        menu_bar.setStyleSheet(STYLES["menu_bar"])

        # Display the first 5 rows of the XLSX file
        self.display_first_5_rows()

    def download_xlsx(self) -> None:
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

        except subprocess.CalledProcessError as subpr_err:
            # If an error occurs during the script execution
            print(f"An error occurred while downloading the file: {subpr_err}")
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while downloading the file: {subpr_err}")

        except FileNotFoundError:
            print("File not found. Please check the path to the script.")
            QMessageBox.critical(self, "Error",
                                 f"File not found. Please check the path to the script.")
        except Exception as gen_err:
            print(f"Unexpected error: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 f"Unexpected error")

    def run_preprocessing(self) -> None:
        """Run the preprocessing script (preprocess.py)."""
        try:
            # Get the directory where the script is being executed
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Build the relative path to the 'preprocess.py' script
            script_path = os.path.join(current_dir, "..", "assets", "preprocess.py")

            # Run the script using the same Python executable that's running the application
            subprocess.run([sys.executable, script_path], check=True)

            # If the preprocessing is successful, display a message
            QMessageBox.information(self, "Preprocessing",
                                    "Data preprocessing completed successfully.")

        except subprocess.CalledProcessError as subpr_err:
            # If an error occurs during the script execution
            print(f"An error occurred while running preprocessing: {subpr_err}")
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while running preprocessing: {subpr_err}")

        except FileNotFoundError:
            print("File not found. Please check the path to the script.")
            QMessageBox.critical(self, "Error",
                                 f"File not found. Please check the path to the script.")
        except Exception as gen_err:
            print(f"Unexpected error: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 f"Unexpected error")

    def display_first_5_rows(self) -> None:
        """Read the first 5 rows of the XLSX file and display them in the table widget."""
        try:
            # Get the directory where the script is being executed
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Build the relative path to the XLSX file
            xlsx_path = os.path.join(current_dir, "..", "assets",
                                     "impulse_buying_data",
                                     "Raw data_Impulse buying behavior.xlsx")

            # Read the XLSX file using pandas
            df = pd.read_excel(xlsx_path)

            # Use the summary function to get the first 5 rows
            first_5_rows = df.head()

            # Set the number of rows and columns in the table widget
            self.table_widget.setRowCount(len(first_5_rows))
            self.table_widget.setColumnCount(len(first_5_rows.columns))
            self.table_widget.setHorizontalHeaderLabels(first_5_rows.columns)

            # Populate the table widget with data
            for row in range(len(first_5_rows)):
                for col in range(len(first_5_rows.columns)):
                    self.table_widget.setItem(row, col,
                                              QTableWidgetItem(str(first_5_rows.iloc[row, col])))

        except Exception as gen_err:
            print(f"An error occurred while reading the XLSX file: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while reading the XLSX file: {gen_err}")
