# Standard library imports
import datetime
import os
import subprocess
import sys

# Third-party imports
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox,
                               QTableWidgetItem, QSizePolicy, QHBoxLayout, QPushButton)

from FinalProject.assets.dashboard_window_setup import (setup_dashboard_window, setup_dashboard_ui,
                                                        setup_dashboard_menu, setup_graph_container)
from FinalProject.assets.graph_widget import GraphWidget
from FinalProject.assets.graphics import question_plot, create_question_combobox
# Local project-specific imports
from FinalProject.styles.styles import STYLES, style_feedback_label


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

        # Initialize the window
        setup_dashboard_window(self)

        # Create the UI components
        setup_dashboard_ui(self)

        # Set up the menu and actions
        setup_dashboard_menu(self)

        # Create container for the graph
        setup_graph_container(self)

        # Display the first 5 rows of the XLSX file
        self.display_tables()

        # Initialize the QComboBox for selecting a question
        self.init_question_combobox()

        self.fig1 = None
        self.fig2 = None

        # Add the buttons inside the graph container, below fig1
        self.add_toggle_buttons()

        # Keep track of the graph states
        self.is_graph_displayed = False
        self.current_graph = None  # Variable to track the current displayed graph
        self.current_distinction = None  # Track the current distinction (gender, school, income)

    def add_toggle_buttons(self) -> None:
        """Create the toggle buttons and add them inside the graph container, in the same row below fig1."""
        # Create the buttons with smaller size
        self.gender_button = QPushButton("Gender", self)
        self.gender_button.setFixedSize(120, 30)
        self.gender_button.setStyleSheet(STYLES["toggle_button"])
        self.gender_button.clicked.connect(self.toggle_graph_by_gender)

        self.school_button = QPushButton("School", self)
        self.school_button.setFixedSize(120, 30)
        self.school_button.setStyleSheet(STYLES["toggle_button"])
        self.school_button.clicked.connect(self.toggle_graph_by_school)

        self.income_button = QPushButton("Income", self)
        self.income_button.setFixedSize(120, 30)
        self.income_button.setStyleSheet(STYLES["toggle_button"])
        self.income_button.clicked.connect(self.toggle_graph_by_income)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(120, 30)
        self.reset_button.setStyleSheet(STYLES["toggle_button"])
        self.reset_button.clicked.connect(self.reset_graph_to_default)

        # Create a layout for the buttons (horizontal layout)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.reset_button)
        buttons_layout.addWidget(self.gender_button)
        buttons_layout.addWidget(self.school_button)
        buttons_layout.addWidget(self.income_button)

        # Create a container for the buttons and add it to the graph container
        buttons_container = QWidget(self)
        buttons_container.setLayout(buttons_layout)
        buttons_container.setSizePolicy(QSizePolicy.Expanding,
                                        QSizePolicy.Fixed)  # Ensure it stretches horizontally but not vertically

        # Add the buttons container to the graph layout
        self.graph_layout.addWidget(buttons_container)

    def reset_graph_to_default(self) -> None:
        """Reset the graph to its default state without any distinctions."""
        self.show_graph()  # Call show_graph without any distinction to show the original graph
        self.current_graph = 'original'  # Set the current graph to original
        self.current_distinction = None  # Reset the distinction
        self.is_graph_displayed = not self.is_graph_displayed  # Toggle the state

    def toggle_graph_by_gender(self) -> None:
        """Toggle between displaying graph by gender and the original graph."""
        if self.current_graph == 'gender':
            # If the graph is currently by gender, revert to the original graph
            self.show_graph()  # Call show_graph without any distinction to show the original graph
            self.current_graph = 'original'  # Set the current graph to original
            self.current_distinction = None  # Reset the distinction
        else:
            # If not, show the graph by gender
            self.show_graph(distinction_by="gender")
            self.current_graph = 'gender'  # Set the current graph to gender
            self.current_distinction = "gender"  # Set the current distinction to gender

        # Toggle the state
        self.is_graph_displayed = not self.is_graph_displayed

    def toggle_graph_by_school(self) -> None:
        """Toggle between displaying graph by school and the original graph."""
        if self.current_graph == 'school':
            # If the graph is currently by school, revert to the original graph
            self.show_graph()
            self.current_graph = 'original'  # Set the current graph to original
            self.current_distinction = None  # Reset the distinction
        else:
            # If not, show the graph by school
            self.show_graph(distinction_by="school")
            self.current_graph = 'school'  # Set the current graph to school
            self.current_distinction = "school"  # Set the distinction to school

        # Toggle the state
        self.is_graph_displayed = not self.is_graph_displayed

    def toggle_graph_by_income(self) -> None:
        """Toggle between displaying graph by income and the original graph."""
        if self.current_graph == 'income':
            # If the current graph is by income, revert to the original graph
            self.show_graph()  # Call show_graph without any distinction to show the original graph
            self.current_graph = 'original'  # Set the current graph to original
            self.current_distinction = None  # Reset the distinction
        else:
            # If not, show the graph by income
            self.show_graph(distinction_by="income")
            self.current_graph = 'income'  # Set the current graph to income
            self.current_distinction = "income"  # Set the distinction to school

        # Toggle the state
        self.is_graph_displayed = not self.is_graph_displayed


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


    def init_question_combobox(self) -> None:
        """Create and initialize the QComboBox for selecting a question."""
        # Use the imported function to create the QComboBox
        self.question_combobox = create_question_combobox(self, self.show_graph)

        # Initially, hide the combobox
        self.question_combobox.setVisible(False)

        # Set the style for the QComboBox
        self.question_combobox.setStyleSheet(STYLES["combo_box"])

        # Add the combobox to the layout (below the welcome label)
        self.central_layout.addWidget(self.question_combobox)


    def show_graph(self, distinction_by: str = None) -> None:
        """Function that shows a graph when 'Graphs' is clicked in the menu or when a specific distinction (gender/school) is requested."""
        selected_question_text = self.question_combobox.currentText()

        # Get the selected question key
        selected_question_key = self.question_combobox.currentData()

        # Print the selected question key and text
        print(f"Selected question key: '{selected_question_key}'")
        print(f"Selected question text: '{selected_question_text}'")

        # If no distinction is provided, keep the previously selected distinction
        if not distinction_by and self.current_distinction:
            distinction_by = self.current_distinction

        # Determine which graph distinction to apply (gender, school, or none)
        if selected_question_key:
            # Default graph (Bar Chart)
            if distinction_by == "gender":
                self.fig1 = question_plot(selected_question_key, distinction_by_gender=True)
                self.fig2 = question_plot(selected_question_key, pie_chart_by_gender=True)
            elif distinction_by == "school":
                self.fig1 = question_plot(selected_question_key, distinction_by_school=True)
            elif distinction_by == "income":
                self.fig1 = question_plot(selected_question_key, distinction_by_income=True)
            else:
                self.fig1 = question_plot(selected_question_key) # Default graph without distinction
                self.fig2 = question_plot(selected_question_key,
                                          pie_chart=True)  # Regular pie chart without distinction

        else:
            self.fig1 = None
            self.fig2 = None

        # Check if the figures are None
        if self.fig1 is None or self.fig2 is None:
            print("The figures were not generated correctly.")
            return

        # Ensure the graph container is visible
        self.graph_widget_container.setVisible(True)

        # Create GraphWidgets to display the graphs
        graph_widget1 = GraphWidget(self.fig1)
        graph_widget2 = GraphWidget(self.fig2)

        # Clear any previous widgets and layouts in the graph layout
        while self.graph_layout.count():
            item = self.graph_layout.takeAt(0)
            # If the item is a widget, delete it
            if item.widget():
                item.widget().deleteLater()
            # If the item is a layout, clear its content and delete it
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                item.layout().deleteLater()

        # Create a horizontal layout to place the graphs side by side
        graphs_layout = QHBoxLayout()
        graphs_layout.addWidget(graph_widget1)
        graphs_layout.addWidget(graph_widget2)

        # Set the layout for the graph container
        self.graph_layout.addLayout(graphs_layout)

        # Add the toggle buttons below the graphs
        self.add_toggle_buttons()

        # Ensure the graph container and the graph adjust properly
        self.graph_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
        self.graph_layout.setSpacing(0)  # Remove space between widgets

        # Make sure the graph widgets occupy the entire available space
        graph_widget1.setMinimumSize(600, 400)  # Adjust the minimum size of the first figure
        graph_widget2.setMinimumSize(600, 400)  # Adjust the minimum size of the second figure

        # Ensure the graph widgets expand both horizontally and vertically
        graph_widget1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graph_widget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graph_widget1.updateGeometry()  # Force the geometry update
        graph_widget2.updateGeometry()  # Force the geometry update

        # Adjust the size of the container if necessary
        self.graph_widget_container.setMinimumSize(1200, 600)  # Adjust minimum size of the container

        # Show the combobox when the "Graphs" menu is clicked
        self.question_combobox.setVisible(True)

    def export_graphs(self) -> None:
        """Export the current graph as an image."""
        try:
            # Get the directory where the files will be saved
            current_dir = os.path.dirname(os.path.abspath(__file__))
            export_dir = os.path.join(current_dir, "..", "assets", "exported_graphs")

            # Create the directory if it doesn't exist
            os.makedirs(export_dir, exist_ok=True)

            # Get the current date and time to avoid overwriting files
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # Define the output file names with a unique timestamp
            file_path1 = os.path.join(export_dir, f"graph1_{timestamp}.png")
            file_path2 = os.path.join(export_dir, f"graph2_{timestamp}.png")

            # Export the graphs using savefig()
            if self.fig1 is not None:
                self.fig1.savefig(file_path1)

            if self.fig2 is not None:
                self.fig2.savefig(file_path2)

            # Notify the user that the graphs have been exported successfully
            QMessageBox.information(self, "Export Successful",
                                    f"The graphs have been exported to:\n{file_path1}\n{file_path2}")

        except Exception as gen_err:
            print(f"Error exporting graphs: {gen_err}")
            QMessageBox.critical(self, "Error", "There was a problem exporting the graphs.")
