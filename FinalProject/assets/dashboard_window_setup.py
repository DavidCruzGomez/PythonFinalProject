"""
Dashboard Setup for PySide6 Application.

This module contains functions to set up the dashboard for a PySide6 application.
The dashboard includes user interface elements, a menu bar, table displays, and a
graph container. Each function focuses on a specific aspect of the setup process.

Key Features:
-------------
1. **Window Configuration**:
   - Dynamically adjusts the window size and position based on the screen dimensions.
   - Centers the window while accounting for taskbars and screen offsets.

2. **User Interface Setup**:
   - Creates a central layout with welcome and feedback labels.
   - Adds table widgets within scrollable areas to display XLSX data.
   - Applies custom styles using a centralized style dictionary.

3. **Menu Bar with Actions**:
   - Includes a "File" menu with actions for home, graphs, download, preprocessing, and export.
   - Supports custom widgets like styled buttons within the menu.

4. **Graph Container**:
   - Adds a graph container to display visualizations.
   - Initially hidden, but can be toggled dynamically.

Functions:
----------
1. `setup_dashboard_window(self) -> None`:
   - Configures the main window's properties, including title, size, and position.

2. `setup_dashboard_ui(self) -> None`:
   - Sets up the central layout, table widgets, and scrollable areas.

3. `setup_dashboard_menu(self) -> None`:
   - Creates and configures the menu bar, including actions and button-based widgets.

4. `setup_graph_container(self) -> None`:
   - Adds a graph container to the central layout for dynamic visualization.
"""
# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget, QApplication,
                               QMenuBar, QWidgetAction, QPushButton,
                               QTableWidget, QScrollArea)

# Local project-specific imports
from FinalProject.styles.styles import STYLES

# Constants
WINDOW_SIZE_FACTOR = 0.8  # Relative size of the window compared to the screen


def setup_dashboard_window(self) -> None:
    """Set up the main window's properties."""
    try:
        # Set the dashboard window's properties
        self.setWindowTitle("Final project David Cruz Gómez")

        # Get the screen size using QScreen
        screen = QApplication.primaryScreen()
        if not screen:
            raise RuntimeError("Unable to retrieve primary screen information.")

        screen_geometry = screen.geometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()

        # Set the window size as a relative value
        window_width = int(screen_width * WINDOW_SIZE_FACTOR)
        window_height = int(screen_height * WINDOW_SIZE_FACTOR)

        # Calculate the position to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Adjust for system taskbars or other offsets
        x_position = max(0, x_position)  # Ensure it doesn't go outside the screen
        y_position = max(0, y_position)  # Ensure it doesn't go outside the screen

        # Set the geometry with the calculated position
        self.setGeometry(x_position, y_position, window_width, window_height)

        print("✅ [SUCCESS] Window setup complete.")

    except RuntimeError as run_err:
        print(f"❌ [ERROR] {run_err}")
    except Exception as gen_err:
        print(f"❌ [ERROR] An unexpected error occurred during window setup: {gen_err}")


def setup_dashboard_ui(self) -> None:
    """Set up the user interface components for dashboard window."""
    try:
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

        # Create a layout for the tables
        table_layout = QVBoxLayout()
        table_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a scroll area to contain the table widget
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.table_widget = QTableWidget()  # Create a table widget to display the XLSX data
        self.scroll_area.setWidget(
            self.table_widget)  # Set the table widget as the widget for the scroll area
        table_layout.addWidget(self.scroll_area)  # Add the scroll area to the layout

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

        print("✅ [SUCCESS] UI setup complete.")

    except Exception as gen_err:
        print(f"❌ [ERROR] Failed to setup UI: {gen_err}")


def setup_dashboard_menu(self) -> None:
    """Set up the menu bar and actions."""
    menu_bar = QMenuBar(self)
    self.setMenuBar(menu_bar)

    # Create the "File" menu
    file_menu = menu_bar.addMenu("File")

    # Create actions for the menu
    home_action = menu_bar.addAction("Home")
    graphs_action = menu_bar.addAction("Graphs")
    download_action = QWidgetAction(self)
    preprocess_action = QWidgetAction(self)

    # Custom actions with buttons
    download_button = QPushButton("Download XLSX")
    download_button.setStyleSheet(STYLES["menu_button"])
    download_button.clicked.connect(self.download_xlsx)
    download_action.setDefaultWidget(download_button)

    preprocess_button = QPushButton("Preprocess XLSX")
    preprocess_button.setStyleSheet(STYLES["menu_button"])
    preprocess_button.clicked.connect(self.run_preprocessing)
    preprocess_action.setDefaultWidget(preprocess_button)

    # Add actions to the menu
    file_menu.addAction(download_action)
    file_menu.addAction(preprocess_action)

    export_action = QWidgetAction(self)
    export_button = QPushButton("Export All Graphs")
    export_button.setStyleSheet(STYLES["menu_button"])
    export_button.clicked.connect(self.export_graphs)  # Connect to the export function
    export_action.setDefaultWidget(export_button)
    file_menu.addAction(export_action)

    # Connect actions to their respective methods
    graphs_action.triggered.connect(self.hide_visibility)
    graphs_action.triggered.connect(self.show_graph)
    home_action.triggered.connect(self.hide_visibility)
    home_action.triggered.connect(self.home_show_visibility)

    # Set the menu bar style
    menu_bar.setStyleSheet(STYLES["menu_bar"])

    print("✅ [SUCCESS] Menu setup complete.")

def setup_graph_container(self) -> None:
    """Add a hidden graph container to the dashboard for visualizations. """
    try:
        # Create a container for the graph within the main layout
        self.graph_widget_container = QWidget(self)  # Container for the graph
        self.graph_widget_container.setObjectName(
            "graph_widget_container")  # Set object name for testing

        # Create and set a vertical layout for the container
        self.graph_layout = QVBoxLayout(self.graph_widget_container)  # Layout for the graph
        self.graph_widget_container.setLayout(self.graph_layout)  # Assign layout

        # Initially, the graph container is not visible
        self.graph_widget_container.setVisible(False)

        # Add the graph container below the menu
        self.central_layout.addWidget(self.graph_widget_container)

        print("✅ [SUCCESS] Graph container setup complete.")

    except Exception as gen_err:
        print(f"❌ [ERROR] Failed to setup graph container: {gen_err}")
        raise
