"""
Unit tests for the `DashboardWindow` class in the `FinalProject.windows.dashboard_window` module.

This test suite verifies the functionality and behavior of the `DashboardWindow` class, which is responsible
for displaying the main dashboard UI. It includes tests for UI initialization, graph toggling based on various
criteria (such as gender, school, and income), file download and preprocessing operations, and the correct
display of tables.

The tests utilize Python's `unittest` framework, and external dependencies like subprocess calls and file I/O
are mocked to simulate different scenarios and verify the correct handling of success and error cases.

Key tests include:
- UI initialization and visibility
- Graph display toggling by gender, school, and income
- Downloading and handling XLSX files
- Running preprocessing tasks and handling exceptions
- Displaying tables with CSV data

This suite ensures that the `DashboardWindow` class behaves as expected under various conditions,
providing a comprehensive check of its core functionality.
"""
import unittest
from unittest.mock import patch, MagicMock

# Third-party imports
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow

# Local project-specific imports
from FinalProject.assets.dashboard_window_setup import (setup_dashboard_ui, setup_dashboard_window,
                                                        setup_dashboard_menu, setup_graph_container)
from FinalProject.windows.dashboard_window import DashboardWindow


class TestDashboardWindow(unittest.TestCase):
    """
    Unit tests for the dashboard window in the `FinalProject.windows.dashboard_window` module.

    This suite verifies the behavior and functionality of the `DashboardWindow` class,
    including UI initialization, graph toggling (by gender, school, income),
    XLSX file download, preprocessing, and table display.

    It tests methods that involve user interactions and background processing,
    with mock objects for subprocess calls and file handling to ensure proper error handling
    and successful operations.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the application instance for testing."""
        cls.app = QApplication([])


    def setUp(self) -> None:
        """Set up the DashboardWindow instance for each test."""
        self.dashboard_window = DashboardWindow()

        setup_dashboard_window(self.dashboard_window)
        setup_dashboard_ui(self.dashboard_window)
        setup_dashboard_menu(self.dashboard_window)
        setup_graph_container(self.dashboard_window)

        self.dashboard_window.init_question_combobox()


    def test_initialization(self) -> None:
        """Test initialization of the DashboardWindow."""
        self.assertIsInstance(self.dashboard_window, QMainWindow)
        self.dashboard_window.show()  # Show the window explicitly in the test
        self.assertTrue(self.dashboard_window.isVisible())


    def test_toggle_graph_by_gender(self) -> None:
        """Test toggling graph by gender."""
        self.dashboard_window.current_graph = 'original'
        self.dashboard_window.toggle_graph_by_gender()
        self.assertEqual(self.dashboard_window.current_graph, 'gender')
        self.assertTrue(self.dashboard_window.is_graph_displayed)


    def test_toggle_graph_by_school(self) -> None:
        """Test toggling graph by school."""
        self.dashboard_window.current_graph = 'original'
        self.dashboard_window.toggle_graph_by_school()
        self.assertEqual(self.dashboard_window.current_graph, 'school')
        self.assertTrue(self.dashboard_window.is_graph_displayed)


    def test_toggle_graph_by_income(self) -> None:
        """Test toggling graph by income."""
        self.dashboard_window.current_graph = 'original'
        self.dashboard_window.toggle_graph_by_income()
        self.assertEqual(self.dashboard_window.current_graph, 'income')
        self.assertTrue(self.dashboard_window.is_graph_displayed)


    @patch('FinalProject.windows.dashboard_window.subprocess.run')
    def test_download_xlsx_success(self, mock_subprocess_run) -> None:
        """Test downloading XLSX file successfully."""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        self.dashboard_window.download_xlsx()
        mock_subprocess_run.assert_called_once()


    @patch('FinalProject.windows.dashboard_window.subprocess.run', side_effect=FileNotFoundError)
    def test_download_xlsx_file_not_found(self, mock_subprocess_run) -> None:
        """Test downloading XLSX file with File Not Found error."""
        with self.assertRaises(FileNotFoundError):
            self.dashboard_window.download_xlsx()


    @patch('FinalProject.windows.dashboard_window.subprocess.run', side_effect=Exception)
    def test_download_xlsx_exception(self, mock_subprocess_run) -> None:
        """Test downloading XLSX file with a general exception."""
        with self.assertRaises(Exception):
            self.dashboard_window.download_xlsx()


    @patch('FinalProject.windows.dashboard_window.subprocess.run')
    def test_run_preprocessing_success(self, mock_subprocess_run) -> None:
        """Test running preprocessing successfully."""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        self.dashboard_window.run_preprocessing()
        mock_subprocess_run.assert_called_once()


    @patch('FinalProject.windows.dashboard_window.subprocess.run', side_effect=FileNotFoundError)
    def test_run_preprocessing_file_not_found(self, mock_subprocess_run) -> None:
        """Test running preprocessing with File Not Found error."""
        with self.assertRaises(FileNotFoundError):
            self.dashboard_window.run_preprocessing()


    @patch('FinalProject.windows.dashboard_window.subprocess.run', side_effect=Exception)
    def test_run_preprocessing_exception(self, mock_subprocess_run) -> None:
        """Test running preprocessing with a general exception."""
        with self.assertRaises(Exception):
            self.dashboard_window.run_preprocessing()


    @patch('FinalProject.windows.dashboard_window.pd.read_csv')
    def test_display_tables_success(self, mock_read_csv) -> None:
        """Test displaying tables successfully."""
        mock_df = pd.DataFrame({'A': [1, 2, 3]})
        mock_read_csv.return_value = mock_df
        self.dashboard_window.display_tables()
        self.assertEqual(self.dashboard_window.table_widget.rowCount(), 3)
        self.assertEqual(self.dashboard_window.table_widget.columnCount(), 1)

if __name__ == '__main__':
    unittest.main()
