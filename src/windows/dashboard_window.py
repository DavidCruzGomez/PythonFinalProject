# Standard library imports
import datetime
import os
import subprocess
import sys

# Third-party imports
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox,
                               QTableWidgetItem, QSizePolicy, QHBoxLayout, QPushButton,
                               QLayout, QComboBox)

# Local project-specific imports
from src.assets.dashboard_window_setup import (setup_dashboard_window, setup_dashboard_ui,
                                               setup_dashboard_menu, setup_graph_container)
from src.assets.graph_widget import GraphWidget
from src.assets.impulse_buying_data.data_dictionary import school, income, gender
from src.styles.styles import STYLES, style_feedback_label
from src.visualization.charts.base import visualize_survey_responses, build_question_selector


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
        self.initialize_question_selection()

        self.fig1 = None
        self.fig2 = None

        # Add the buttons inside the graph container, below fig1
        self.add_toggle_buttons()

        # Keep track of the graph states
        self.current_graph = None  # Variable to track the current displayed graph
        self.current_distinction = None  # Track the current distinction (gender, school, income)

        self.gender_filter_buttons = None

    def _handle_income_filter(self, income_category: str, button: QPushButton):
        """Updates the chart with the selected income filter."""
        # Reset styles for all buttons
        for btn in self.income_buttons:
            btn.setStyleSheet(STYLES["toggle_button"])
            btn.setFixedSize(150, 35)

        # Apply style to the active button
        button.setStyleSheet(STYLES["active_toggle_button"])

        # Update the chart
        self.update_income_pie_chart(income_category)

    def create_income_filter_buttons(self) -> QWidget:
        """Creates buttons for each income category."""
        from src.assets.impulse_buying_data.data_dictionary import income

        filter_layout = QVBoxLayout()
        filter_layout.setContentsMargins(10, 0, 10, 0)

        self.income_buttons = []
        income_categories = list(income.values())

        filter_layout.addWidget(QLabel("Filter by:"))

        for category in income_categories:
            button = QPushButton(category)
            button.setFixedSize(150, 35)
            button.setStyleSheet(STYLES["toggle_button"])
            # Connect the signal, passing the button as an argument
            button.clicked.connect(
                lambda checked, cat=category, b=button: self._handle_income_filter(cat, b))
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            filter_layout.addWidget(button)
            self.income_buttons.append(button)

        filter_layout.addStretch()

        # Set initial style for the first button
        if self.income_buttons:
            self.income_buttons[0].setStyleSheet(STYLES["active_toggle_button"])
            # Update the chart with the first income category
            self.update_income_pie_chart(income_categories[0])

        container = QWidget()
        container.setLayout(filter_layout)
        return container

    def update_income_pie_chart(self, selected_income: str) -> None:
        """Updates the pie chart with the selected income category."""
        selected_question = self.question_combobox.currentData()

        new_fig2 = visualize_survey_responses(
            selected_question,
            pie_chart_by_income=True,
            income_filter=selected_income
        )

        if self.graph_layout.count() == 0:
            return

        main_item = self.graph_layout.itemAt(0)
        if not main_item or not main_item.layout():
            return

        main_layout = main_item.layout()
        charts_container = None
        for i in range(main_layout.count()):
            item = main_layout.itemAt(i)
            if isinstance(item, QHBoxLayout):
                charts_container = item
                break

        if not charts_container:
            return

        if charts_container.count() >= 2:
            old_pie = charts_container.itemAt(1).widget()
            if old_pie:
                old_pie.deleteLater()

        self.graph_widget2 = GraphWidget(new_fig2)
        if charts_container.count() >= 1:
            charts_container.insertWidget(1, self.graph_widget2)
        else:
            charts_container.addWidget(self.graph_widget2)

        self.fig2 = new_fig2
        self.graph_widget2.draw()


    def _handle_school_filter(self, school: str):
        """Updates the chart with the selected school filter."""
        self.update_school_pie_chart(school)

    def create_school_filter_combobox(self) -> QWidget:
        """Creates a combo box to select schools."""
        filter_layout = QVBoxLayout()

        self.school_combobox = QComboBox()
        self.school_combobox.addItems(
            list(school.values()))  # Assumes 'school' is an imported dictionary
        self.school_combobox.currentTextChanged.connect(self._handle_school_filter)
        self.school_combobox.setStyleSheet(STYLES["combo_box"])

        filter_layout.addWidget(QLabel("Filter by school:"))
        filter_layout.addWidget(self.school_combobox)

        filter_layout.addStretch()

        container = QWidget()
        container.setLayout(filter_layout)
        return container

    def update_school_pie_chart(self, selected_school: str) -> None:
        """Updates the pie chart with the selected school."""
        selected_question = self.question_combobox.currentData()

        # Generate a new chart
        new_fig2 = visualize_survey_responses(
            selected_question,
            pie_chart_by_school=True,
            school_filter=selected_school
        )

        # Safely access the layout
        if self.graph_layout.count() == 0:
            return

        main_item = self.graph_layout.itemAt(0)
        if not main_item or not main_item.layout():
            return

        main_layout = main_item.layout()

        # Properly find the tests_charts container
        charts_container = None
        for i in range(main_layout.count()):
            item = main_layout.itemAt(i)
            if isinstance(item, QHBoxLayout):  # The layout that contains the tests_charts
                charts_container = item
                break

        if not charts_container:
            return

        # Remove the old chart if it exists
        if charts_container.count() >= 2:
            old_pie = charts_container.itemAt(1).widget()
            if old_pie:
                old_pie.deleteLater()

        # Insert the new chart
        self.graph_widget2 = GraphWidget(new_fig2)
        if charts_container.count() >= 1:
            charts_container.insertWidget(1, self.graph_widget2)
        else:
            charts_container.addWidget(self.graph_widget2)

        self.fig2 = new_fig2
        self.graph_widget2.draw()

    def _handle_gender_filter(self, gender: str):
        """Updates the pie chart with the selected gender filter"""
        # Reset button styles
        self.male_btn.setStyleSheet(STYLES["toggle_button"])
        self.female_btn.setStyleSheet(STYLES["toggle_button"])

        # Apply style to the active button
        if gender == "Male":
            self.male_btn.setStyleSheet(STYLES["active_toggle_button"])
        else:
            self.female_btn.setStyleSheet(STYLES["active_toggle_button"])

        # Update the chart
        self.update_pie_chart(gender)

    def create_gender_filter_buttons(self) -> QWidget:
        """Creates filter buttons with enhanced styling"""
        filter_layout = QVBoxLayout()
        filter_layout.setContentsMargins(10, 0, 10, 0)

        # Male button
        self.male_btn = QPushButton("Male")
        self.male_btn.setFixedSize(130, 35)
        self.male_btn.setStyleSheet(STYLES["toggle_button"])
        self.male_btn.clicked.connect(lambda: self._handle_gender_filter("Male"))
        self.male_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # Female button
        self.female_btn = QPushButton("Female")
        self.female_btn.setFixedSize(130, 35)
        self.female_btn.setStyleSheet(STYLES["toggle_button"])
        self.female_btn.clicked.connect(lambda: self._handle_gender_filter("Female"))
        self.female_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        filter_layout.addWidget(QLabel("Filter by:"))
        filter_layout.addWidget(self.male_btn)
        filter_layout.addWidget(self.female_btn)
        filter_layout.addStretch()

        container = QWidget()
        container.setLayout(filter_layout)

        # Add at the end of the method
        if self.current_distinction == "gender":
            self.male_btn.setStyleSheet(STYLES["active_toggle_button"])
            
        return container

    def update_pie_chart(self, gender: str) -> None:
        selected_question_key = self.question_combobox.currentData()

        # Generate new pie chart
        new_fig2 = visualize_survey_responses(
            selected_question_key,
            pie_chart_by_gender=True,
            gender_filter=gender
        )

        # Get the graphs container
        main_layout = self.graph_layout.itemAt(0).layout()  # Main layout (QHBoxLayout)
        graphs_container = main_layout.itemAt(0).layout()  # First child: QHBoxLayout of tests_charts

        # Remove the old pie chart (position 1)
        if graphs_container.count() >= 2:
            old_pie = graphs_container.itemAt(1).widget()
            if old_pie:
                graphs_container.removeWidget(old_pie)
                old_pie.deleteLater()

        # Add the new pie chart at position 1 (to the right of the bars)
        self.graph_widget2 = GraphWidget(new_fig2)
        graphs_container.insertWidget(1, self.graph_widget2)

        # Update and redraw
        self.fig2 = new_fig2
        self.graph_widget2.draw()

    def add_toggle_buttons(self) -> None:
        """Create the toggle buttons and add them inside the graph container, in the same row below fig1."""
        # Create the buttons with smaller size
        self.gender_button = QPushButton("Gender", self)
        self.gender_button.setFixedSize(120, 30)
        self.gender_button.setStyleSheet(STYLES["toggle_button"])
        self.gender_button.clicked.connect(lambda: self.toggle_graph("gender", gender))
        self.gender_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.school_button = QPushButton("School", self)
        self.school_button.setFixedSize(120, 30)
        self.school_button.setStyleSheet(STYLES["toggle_button"])
        self.school_button.clicked.connect(lambda: self.toggle_graph("school", school))
        self.school_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.income_button = QPushButton("Income", self)
        self.income_button.setFixedSize(120, 30)
        self.income_button.setStyleSheet(STYLES["toggle_button"])
        self.income_button.clicked.connect(lambda: self.toggle_graph("income", income))
        self.income_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(120, 30)
        self.reset_button.setStyleSheet(STYLES["toggle_button"])
        self.reset_button.clicked.connect(self.reset_graph_to_default)
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)

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
        self.current_graph = 'original'  # Set the current graph to original
        self.current_distinction = None  # Reset the distinction
        self.show_graph(
            distinction_by=None)  # Call show_graph without any distinction to show the original graph

    def toggle_graph(self, graph_type: str, filters: dict) -> None:
        """
        Toggle between displaying a specialized graph view and the original/default view.
        Handles graph state management and UI synchronization for filter controls.
        :param graph_type: Type of distinction to apply.
            Valid values: 'gender', 'school', 'income'
        :param filters: Dictionary containing default filter values for each graph type.
            Format: {graph_type: default_filter_value}
        """
        # Check if requested graph type is already active
        if self.current_graph == graph_type:
            # If already in the specified graph type, revert to the original graph
            self.current_graph = 'original'
            self.current_distinction = None # Clear active distinction
            self.show_graph()
        else:
            # Otherwise, display the graph by the specified type
            self.current_graph = graph_type         # Set current active graph type
            self.current_distinction = graph_type   # Track active distinction category

            # Get the default filter value for the graph type
            default_filter_value = list(filters.values())[0]

            # Show the graph with the default filter
            self.show_graph(
                distinction_by=graph_type,
                **{f"{graph_type}_filter": default_filter_value}
            )
            # Handle UI updates based on the graph type
            if graph_type == "gender":
                self._handle_gender_filter("Male")
            elif graph_type == "school" and hasattr(self, 'school_combobox'):
                self.school_combobox.setCurrentText(default_filter_value)


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
            print(f"❌ [ERROR] An error occurred while downloading the file: {subpr_err}")
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while downloading the file: {subpr_err}")

        except FileNotFoundError:
            print("❌ [ERROR] File not found. Please check the path to the script.")
            QMessageBox.critical(self, "Error",
                                 "File not found. Please check the path to the script.")
            raise FileNotFoundError("❌ [ERROR] File not found. Please check the path to the script.")
        except Exception as gen_err:
            print(f"Unexpected error: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 "Unexpected error")
            raise gen_err(f"❌ [ERROR] Unexpected error: {gen_err}")

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
            print(f"❌ [ERROR] An error occurred while running preprocessing: {subpr_err}")
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while running preprocessing: {subpr_err}")

        except FileNotFoundError:
            print("❌ [ERROR] File not found. Please check the path to the script.")
            QMessageBox.critical(self, "Error",
                                 "File not found. Please check the path to the script.")
            raise FileNotFoundError("❌ [ERROR] File not found. Please check the path to the script.")
        except Exception as gen_err:
            print(f"Unexpected error: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 "Unexpected error")
            raise gen_err(f"❌ [ERROR] Unexpected error: {gen_err}")

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
            print(f"❌ [ERROR] An error occurred while reading the CSV files: {gen_err}")
            QMessageBox.critical(self, "Error",
                                 f"❌ [ERROR] An error occurred while reading the CSV files: {gen_err}")


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


    def initialize_question_selection(self) -> None:
        """Create and initialize the QComboBox for selecting a question."""
        # Use the imported function to create the QComboBox
        self.question_combobox = build_question_selector(self, self.show_graph)

        # Initially, hide the combobox
        self.question_combobox.setVisible(False)

        # Set the style for the QComboBox
        self.question_combobox.setStyleSheet(STYLES["combo_box"])

        # Add the combobox to the layout (below the welcome label)
        self.central_layout.addWidget(self.question_combobox)

    def show_graph(self, distinction_by: str = None,
                   gender_filter: str = None,
                   school_filter: str = None,
                   income_filter: str = None) -> None:
        """Displays main and secondary graphs based on current selection and filters.

        Args:
            distinction_by: Distinction type to apply (gender/school/income)
            gender_filter: Specific gender filter for pie chart
        """
        # Get current selection
        selected_question_key = self.question_combobox.currentData()
        selected_question_text = self.question_combobox.currentText()

        self._log_selection(selected_question_key, selected_question_text)
        distinction_by = distinction_by if distinction_by is not None else self.current_distinction

        # Generate tests_visualization figures
        self._generate_visualization_figures(selected_question_key, distinction_by, gender_filter)
        if not self._validate_figure_creation():
            return

        # Configure UI elements
        self._prepare_graph_display_area()
        self._refresh_graph_interface(distinction_by)

    def _log_selection(self, key: str, text: str) -> None:
        """Logs current selection for debugging purposes."""
        print(f"Selected question - Key: '{key}', Text: '{text}'")

    def _resolve_distinction_type(self, distinction: str) -> str:
        """Determines distinction type using previous state if needed."""
        return distinction or self.current_distinction

    def _generate_visualization_figures(
            self,
            question_key: str,
            distinction: str,
            gender_filter: str,
            school_filter: str = None,
            income_filter: str = None
    ) -> None:
        """Generates tests_visualization figures based on current parameters."""
        # Main chart configuration
        if distinction == "gender":
            self.fig1 = visualize_survey_responses(question_key, distinction_by_gender=True)
        elif distinction == "school":
            self.fig1 = visualize_survey_responses(question_key, distinction_by_school=True)
        elif distinction == "income":
            self.fig1 = visualize_survey_responses(question_key, distinction_by_income=True)
        else:
            self.fig1 = visualize_survey_responses(question_key)

        # Secondary chart configuration
        if distinction == "gender":
            self.fig2 = visualize_survey_responses(
                question_key,
                pie_chart_by_gender=True,
                gender_filter=gender_filter or "Male"  # Default to Male
            )
        elif distinction == "school":
            self.fig2 = visualize_survey_responses(
                question_key,
                pie_chart_by_school=True,
                school_filter=school_filter or list(school.values())[0]
            )
        elif distinction == "income":
            self.fig2 = visualize_survey_responses(
                question_key,
                pie_chart_by_income=True,
                income_filter=income_filter or list(income.values())[0]
            )
        else:
            # Regular pie chart for non-gender distinctions
            self.fig2 = visualize_survey_responses(question_key, pie_chart=True)

    def _validate_figure_creation(self) -> bool:
        """Validates successful figure generation."""
        if None in (self.fig1, self.fig2):
            print("❌ [ERROR] Error: Failed to generate tests_visualization figures")
            return False
        return True

    def _prepare_graph_display_area(self) -> None:
        """Prepares graph container for new content."""
        self.graph_widget_container.setVisible(True)
        self._clear_previous_visualizations()

    def _clear_previous_visualizations(self) -> None:
        """Clears existing tests_visualization elements from layout."""
        while self.graph_layout.count():
            item = self.graph_layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()
            elif layout := item.layout():
                self._recursive_layout_cleanup(layout)

    def _recursive_layout_cleanup(self, layout: QLayout) -> None:
        """Recursively removes elements from a layout."""
        while layout.count():
            sub_item = layout.takeAt(0)
            if sub_widget := sub_item.widget():
                sub_widget.deleteLater()
            elif sub_layout := sub_item.layout():
                self._recursive_layout_cleanup(sub_layout)
        layout.deleteLater()

    def _refresh_graph_interface(self, distinction: str) -> None:
        """Updates UI with new visualizations and controls."""
        # Create graph widgets
        graph_widgets = self._initialize_graph_components()

        # Build main layout structure
        main_layout = QHBoxLayout()

        # Horizontal layout for tests_charts
        charts_layout = QHBoxLayout()
        charts_layout.addWidget(graph_widgets[0])
        charts_layout.addWidget(graph_widgets[1])

        # Add filter controls when needed
        if distinction == "gender":
            charts_layout.addWidget(
                self.create_gender_filter_buttons())

        elif distinction == "school":
            filter_widget = self.create_school_filter_combobox()
            charts_layout.addWidget(filter_widget)

        elif distinction == "income":
            filter_widget = self.create_income_filter_buttons()
            charts_layout.addWidget(filter_widget)

        main_layout.addLayout(charts_layout)
        self._complete_interface_setup(main_layout, graph_widgets)

    def _initialize_graph_components(self) -> tuple:
        """Creates and configures graph widgets."""
        primary_graph = GraphWidget(self.fig1)
        secondary_graph = GraphWidget(self.fig2)

        # Common widget configuration
        for widget in (primary_graph, secondary_graph):
            widget.setMinimumSize(600, 400)
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.updateGeometry()

        return primary_graph, secondary_graph

    def _arrange_graph_components(self, widgets: tuple) -> QHBoxLayout:
        """Creates horizontal layout for graph display."""
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(widgets[0])
        layout.addWidget(widgets[1])
        return layout

    def _complete_interface_setup(self, layout: QHBoxLayout, widgets: tuple) -> None:
        """Finalizes UI configuration."""
        self.graph_layout.addLayout(layout)
        self.add_toggle_buttons()
        self._apply_final_layout_config()

        # Ensure question selector visibility
        self.question_combobox.setVisible(True)

    def _apply_final_layout_config(self) -> None:
        """Applies final layout properties for optimal display."""
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        self.graph_layout.setSpacing(0)
        self.graph_widget_container.setMinimumSize(1200, 600)

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
            print(f"❌ [ERROR] Error exporting graphs: {gen_err}")
            QMessageBox.critical(self, "Error", "There was a problem exporting the graphs.")
