"""
Unit tests for the `DashboardWindowSetup` functions in the
`FinalProject.assets.dashboard_window_setup` module.

This test suite ensures that the functions responsible for setting up the main dashboard window,
its user interface, menu, and graph container are functioning correctly. Each function is tested to
verify that it properly configures the components of the `QMainWindow` and its layout, including the
menu, UI elements, and graph container visibility.

Key tests include:

- Dashboard Window Setup:
    - `setup_dashboard_window`:
        - Verifies that the dashboard window is properly initialized with the correct window title
          and appropriate dimensions.

- Dashboard UI Setup:
    - `setup_dashboard_ui`:
        - Ensures that the central widget and layout are correctly set up for the dashboard window,
          with the expected number of layout items.

- Dashboard Menu Setup:
    - `setup_dashboard_menu`:
        - Tests the creation and setup of the dashboard's menu bar, verifying that the menu bar is
          present and contains the correct first action (e.g., "File").

- Graph Container Setup:
    - `setup_graph_container`:
        - Verifies that the graph container is correctly added to the dashboard window
          and is initially hidden as expected. It ensures that the graph widget container is
          a child of the main window and that it can be properly referenced.

Each test ensures that the individual setup functions for the dashboard window are robust, correctly
setting up the application’s user interface and components, providing the expected functionality,
and behaving correctly under various conditions.
"""
# Standard library imports
import unittest

# Third-party imports
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

# Local project-specific imports
from FinalProject.assets.dashboard_window_setup import (
    setup_dashboard_window,
    setup_dashboard_ui,
    setup_dashboard_menu,
    setup_graph_container,
)


class TestDashboardWindowSetup(unittest.TestCase):
    """
    Unit tests for the setup functions of the `DashboardWindow` class in the
    `FinalProject.assets.dashboard_window_setup` module.

    This suite verifies the behavior and correctness of various setup functions
    responsible for configuring the main window, UI components, menus, and graph containers.

    It includes tests for the following setup functions:
    - `setup_dashboard_window`: Ensures the window is correctly initialized with a title and dimensions.
    - `setup_dashboard_ui`: Verifies the proper creation of the central widget and its layout.
    - `setup_dashboard_menu`: Confirms that the menu bar is set up with the expected actions.
    - `setup_graph_container`: Ensures the graph container is initialized and hidden correctly.

    Mocking is used to bypass certain UI-related actions, ensuring a controlled test environment.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the application instance for testing."""
        cls.app = QApplication([])

    def setUp(self) -> None:
        """Set up the main window for each test."""
        self.dashboard_window = QMainWindow()

        # Add the required methods to the main window
        self.dashboard_window.download_xlsx = lambda: None
        self.dashboard_window.run_preprocessing = lambda: None
        self.dashboard_window.export_graphs = lambda: None
        self.dashboard_window.hide_visibility = lambda: None
        self.dashboard_window.show_graph = lambda: None
        self.dashboard_window.home_show_visibility = lambda: None

        # Ensure the central layout is set up
        setup_dashboard_ui(self.dashboard_window)

    def test_setup_dashboard_window(self) -> None:
        """Test the setup_dashboard_window function."""
        setup_dashboard_window(self.dashboard_window)
        self.assertEqual(self.dashboard_window.windowTitle(), "Final project David Cruz Gómez")
        self.assertTrue(self.dashboard_window.geometry().width() > 0)
        self.assertTrue(self.dashboard_window.geometry().height() > 0)

    def test_setup_dashboard_ui(self) -> None:
        """Test the setup_dashboard_ui function."""
        setup_dashboard_ui(self.dashboard_window)
        self.assertIsNotNone(self.dashboard_window.centralWidget())
        self.assertEqual(self.dashboard_window.centralWidget().layout().count(), 3)

    def test_setup_dashboard_menu(self) -> None:
        """Test the setup_dashboard_menu function."""
        setup_dashboard_menu(self.dashboard_window)
        menu_bar = self.dashboard_window.menuBar()
        self.assertIsNotNone(menu_bar)
        self.assertEqual(menu_bar.actions()[0].text(), "File")

    def test_setup_graph_container(self) -> None:
        """Test the setup_graph_container function."""
        setup_graph_container(self.dashboard_window)
        graph_widget_container = self.dashboard_window.findChild(
            QWidget, "graph_widget_container"
        )
        self.assertIsNotNone(graph_widget_container,
                             "graph_widget_container was not found in the dashboard window")
        self.assertTrue(graph_widget_container.isHidden(),
                        "graph_widget_container should initially be hidden")

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up the application instance after testing."""
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()