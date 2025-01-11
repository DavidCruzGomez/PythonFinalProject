# Standard library imports
import os
import subprocess
import sys

# Third-party imports
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication,
                               QMenuBar, QMessageBox, QWidgetAction, QPushButton,
                               QTableWidget, QTableWidgetItem, QScrollArea,
                               QSizePolicy, QComboBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from FinalProject.assets.graphics import question_plot, create_question_combobox

# Local project-specific imports
from FinalProject.styles.styles import STYLES, style_feedback_label


class GraphWidget(FigureCanvas):
    def __init__(self, fig):
        # Call the base constructor of FigureCanvas with the figure
        super().__init__(fig)

        # Configure the size and geometry of the widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

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
        self.central_layout = QVBoxLayout()
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.central_layout.setContentsMargins(20, 20, 20,
                                          20)  # Adjust margins (left, top, right, bottom)
        self.central_layout.setSpacing(10)

        # Add a welcome label
        self.welcome_label = QLabel("Welcome to the Dashboard!")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet(STYLES["title"])
        self.central_layout.addWidget(self.welcome_label)

        # Add a feedback label for displaying messages to the user (e.g., success or errors)
        self._feedback_label = QLabel("")  # Initially empty
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_layout.addWidget(self._feedback_label)

        # Create a layout for the table
        table_layout = QVBoxLayout()
        table_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a scroll area to contain the table widget
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.table_widget = QTableWidget() # Create a table widget to display the XLSX data
        self.scroll_area.setWidget(self.table_widget) # Set the table widget as the widget for the scroll area
        table_layout.addWidget(self.scroll_area) # Add the scroll area to the layout

        # Create the second scroll area for the second table
        self.scroll_area_processed = QScrollArea()
        self.scroll_area_processed.setWidgetResizable(True)
        self.table_widget_processed = QTableWidget()
        self.scroll_area_processed.setWidget(self.table_widget_processed)
        table_layout.addWidget(self.scroll_area_processed)

        # Add the table layout to the central layout
        self.central_layout.addLayout(table_layout)

        # Set the scroll area style
        self.scroll_area.setStyleSheet(STYLES["scroll_area"])
        self.scroll_area_processed.setStyleSheet(STYLES["scroll_area"])

        # Set the layout to a central widget
        central_widget = QWidget()
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)

        # Create a menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Add a "File" menu
        file_menu = menu_bar.addMenu("File")
        home_action = menu_bar.addAction("Home")
        graphs_action = menu_bar.addAction("Graphs")

        graphs_action.triggered.connect(self.hide_visibility)
        graphs_action.triggered.connect(self.show_graph)

        home_action.triggered.connect(self.hide_visibility)
        home_action.triggered.connect(self.home_show_visibility)

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

        # Create a container for the graph within the main layout
        self.graph_widget_container = QWidget(self)  # Container for the graph
        self.graph_layout = QVBoxLayout(self.graph_widget_container)  # Layout for the graph
        self.graph_widget_container.setLayout(self.graph_layout)  # Assign layout

        # Initially, the graph container is not visible
        self.graph_widget_container.setVisible(False)

        # Add the graph container below the menu
        self.central_layout.addWidget(self.graph_widget_container)

        # Display the first 5 rows of the XLSX file
        self.display_tables()

        # Initialize the QComboBox for selecting a question
        self.init_question_combobox()


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
                                 "File not found. Please check the path to the script.")
        except Exception as gen_err:
            print(f"Unexpected error: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 "Unexpected error")

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

            self.display_tables()

            self._feedback_label.setText("")

        except subprocess.CalledProcessError as subpr_err:
            # If an error occurs during the script execution
            print(f"An error occurred while running preprocessing: {subpr_err}")
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while running preprocessing: {subpr_err}")

        except FileNotFoundError:
            print("File not found. Please check the path to the script.")
            QMessageBox.critical(self, "Error",
                                 "File not found. Please check the path to the script.")
        except Exception as gen_err:
            print(f"Unexpected error: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 "Unexpected error")

    def display_tables(self) -> None:
        """Read the first 5 rows of the 'cleaned_data.csv' file and display them in the first table,
           and display all rows of the 'processed_data.csv' file in the second table."""

        # Get the directory where the script is being executed
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the relative paths to the CSV files
        cleaned_csv_path = os.path.join(current_dir, "..", "assets", "impulse_buying_data",
                                        "cleaned_data.csv")
        processed_csv_path = os.path.join(current_dir, "..", "assets", "impulse_buying_data",
                                          "processed_data.csv")

        try:
            # --- First Table: Cleaned Data ---
            # Process cleaned_data.csv (first 5 rows)
            if os.path.exists(cleaned_csv_path):
                # Read the cleaned data CSV file using pandas
                cleaned_df = pd.read_csv(cleaned_csv_path)

                # Use the summary function to get the first 5 rows
                first_5_rows = cleaned_df.head()

                # Create a layout for the first table block
                table1_block_layout = QVBoxLayout()

                # Add a label for the first table (Dataframe Preview)
                self.dataframe_label = QLabel("Dataframe Preview")
                self.dataframe_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.dataframe_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
                table1_block_layout.addWidget(self.dataframe_label)

                # Set the number of rows and columns in the first table widget
                self.table_widget.setRowCount(len(first_5_rows))
                self.table_widget.setColumnCount(len(first_5_rows.columns))
                self.table_widget.setHorizontalHeaderLabels(first_5_rows.columns)

                # Populate the first table widget with data
                for row in range(len(first_5_rows)):
                    for col in range(len(first_5_rows.columns)):
                        self.table_widget.setItem(row, col,
                                                    QTableWidgetItem(
                                                        str(first_5_rows.iloc[row, col])))

                # Add the table to the block layout
                table1_block_layout.addWidget(self.scroll_area)

                # Create a container for the first table block
                table1_block_container = QWidget()
                table1_block_container.setLayout(table1_block_layout)

                # Center the block inside a layout
                table1_block_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Insert the container into the main layout
                self.central_layout.insertWidget(1, table1_block_container)

            else:
                style_feedback_label(self._feedback_label,
                                     "The cleaned dataset has not been found", "error")

            # --- Second Table: Processed Data ---
            if os.path.exists(processed_csv_path):
                # Read the processed data CSV file using pandas
                processed_df = pd.read_csv(processed_csv_path)

                # Create a layout for the second table block
                table2_block_layout = QVBoxLayout()

                # Add a label for the second table (Processed Data Preview)
                self.processed_data_label = QLabel("Descriptive Statistics")
                self.processed_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.processed_data_label.setStyleSheet(
                    "font-size: 24px; font-weight: bold; color: #333;")
                table2_block_layout.addWidget(self.processed_data_label)

                # Set the number of rows and columns in the second table widget
                self.table_widget_processed.setRowCount(len(processed_df))
                self.table_widget_processed.setColumnCount(len(processed_df.columns))
                self.table_widget_processed.setHorizontalHeaderLabels(processed_df.columns)

                # Populate the second table widget with data (all rows of processed_data)
                for row in range(len(processed_df)):
                    for col in range(len(processed_df.columns)):
                        self.table_widget_processed.setItem(row, col,
                                                    QTableWidgetItem(
                                                        str(processed_df.iloc[row, col])))

                # Add the table to the block layout
                table2_block_layout.addWidget(self.scroll_area_processed)

                # Create a container for the second table block
                table2_block_container = QWidget()
                table2_block_container.setLayout(table2_block_layout)

                # Center the block inside a layout
                table2_block_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Insert the container into the main layout
                self.central_layout.insertWidget(2, table2_block_container)


            else:
                style_feedback_label(self._feedback_label,
                                     "The processed dataset has not been found", "error")

        except Exception as gen_err:
            print(f"An error occurred while reading the CSV files: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while reading the CSV files: {gen_err}")


    def hide_visibility(self) -> None:
        """Hide the visibility of the title and the table widget."""
        self.welcome_label.setVisible(False)
        self.table_widget.setVisible(False)
        self.table_widget_processed.setVisible(False)
        self.scroll_area_processed.setVisible(False)
        self.scroll_area.setVisible(False)
        self.graph_widget_container.setVisible(False)

        # Hide table headers
        self.dataframe_label.setVisible(False)
        self.processed_data_label.setVisible(False)

        # Hide the question combobox
        self.question_combobox.setVisible(False)

    def home_show_visibility(self) -> None:
        """Display the visibility of the title and the table widget."""
        self.welcome_label.setVisible(True)
        self.table_widget.setVisible(True)
        self.table_widget_processed.setVisible(True)
        self.scroll_area_processed.setVisible(True)
        self.scroll_area.setVisible(True)

        # Show table headers
        self.dataframe_label.setVisible(True)
        self.processed_data_label.setVisible(True)


    def init_question_combobox(self):
        """Create and initialize the QComboBox for selecting a question."""
        # Use the imported function to create the QComboBox
        self.question_combobox = create_question_combobox(self, self.show_graph)

        # Initially, hide the combobox
        self.question_combobox.setVisible(False)

        # Set the style for the QComboBox
        self.question_combobox.setStyleSheet(STYLES["combo_box"])

        # Add the combobox to the layout (below the welcome label)
        self.central_layout.addWidget(self.question_combobox)


    def show_graph(self):
        """Function tha shows a graph when 'Graphs' is clicked in the menu."""
        selected_question_text = self.question_combobox.currentText()

        # Get the selected question key
        selected_question_key = self.question_combobox.currentData()  # Esta es la clave (key)

        # Print the selected question key and text
        print(f"Selected question key: '{selected_question_key}'")
        print(f"Selected question text: '{selected_question_text}'")

        # Call the `question_plot` function with the selected key
        if selected_question_key:
            fig = question_plot(selected_question_key)
        else:
            fig = None

        # Check if the figure is None
        if fig is None:
            print("The figure was not generated correctly.")
            return

        # Display the graph container in the main window
        self.graph_widget_container.setVisible(True)

        # Create a GraphWidget to display the graph
        graph_widget = GraphWidget(fig)

        # Clear any previous graph from the layout and add the new one
        for i in reversed(range(self.graph_layout.count())):
            widget = self.graph_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Remove the previous widget

        # Set the layout for the graph container
        self.graph_layout.addWidget(graph_widget)

        # Ensure the graph container and the graph adjust properly
        self.graph_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
        self.graph_layout.setSpacing(0)  # Remove space between widgets

        # Make sure the graph widget occupies the entire available space
        graph_widget.setMinimumSize(600, 400)  # Adjust the minimum size of the figure

        # Ensure the graph widget expands both horizontally and vertically
        graph_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graph_widget.updateGeometry()  # Force the geometry update

        # Adjust the size of the container if necessary
        self.graph_widget_container.setMinimumSize(800, 600)  # Adjust minimum size of the container

        # Show the combobox when the "Graphs" menu is clicked
        self.question_combobox.setVisible(True)
