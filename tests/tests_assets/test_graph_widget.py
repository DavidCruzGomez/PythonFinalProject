"""
Unit tests for the `GraphWidget` class in the `FinalProject.assets.graph_widget` module.

This test suite ensures that the custom widget, which integrates a Matplotlib figure
with PySide6 for user interactions, behaves as expected under various conditions.
Each method of the `GraphWidget` class is tested to verify correct functionality,
including user interactions, keyboard shortcuts, and mouse events.

Key tests include:

- Initialization:
    - Verifies that the `GraphWidget` initializes correctly, with all attributes
      in their expected default state.

- Keyboard Interactions:
    - Tests keyboard shortcuts like resetting zoom, saving the figure, showing help,
      toggling the grid, and panning the view. Each key press is validated to ensure
      it triggers the correct action.

- Mouse Interactions:
    - `on_click`: Tests handling of valid and invalid mouse click events, ensuring
      the widget enters dragging mode only when appropriate.
    - `on_release`: Confirms that dragging mode is correctly disabled on mouse release.
    - `on_move`: Verifies panning functionality when dragging is enabled.

- Other Functionalities:
    - `reset_zoom`: Ensures the widget correctly resets the view to its default zoom.
    - `toggle_grid`: Verifies the ability to toggle the grid display on or off.
    - `save_figure`: Tests saving the figure to a file, including handling user cancellations.
    - `show_help`: Validates the help message display with accurate content.

Each test is designed to address both normal behavior and edge cases, ensuring the
`GraphWidget` is robust and reliable during real-world use.
"""
# Standard library imports
import unittest
from unittest.mock import MagicMock, patch

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from matplotlib.figure import Figure

# Local project-specific imports
from FinalProject.assets.graph_widget import GraphWidget


class TestGraphWidget(unittest.TestCase):
    """
    Unit tests for the GraphWidget class.

    This class verifies that the custom GraphWidget behaves as expected,
    including user interactions and event handling.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Initialize the QApplication instance once for all tests,
        as it is required to test PySide6 widgets.
        """
        cls.app: QApplication = QApplication([])


    def setUp(self) -> None:
        """
        Set up the GraphWidget instance for each test.
        """
        self.fig: Figure = Figure()
        self.widget: GraphWidget = GraphWidget(self.fig)


    def test_initialization(self) -> None:
        """
        Test that the GraphWidget is initialized correctly.
        """
        self.assertIsNotNone(self.widget) # The widget should not be None
        # The widget should not be in dragging mode initially
        self.assertTrue(self.widget._dragging is False)
        self.assertIsNone(self.widget._last_x) # There should be no previous x-coordinate
        self.assertIsNone(self.widget._last_y) # There should be no previous y-coordinate


    def test_keyPressEvent(self) -> None:
        """
        Test keyboard shortcuts and their corresponding actions.
        """
        # Mock methods to check if they are called correctly
        self.widget.reset_zoom = MagicMock()
        self.widget.save_figure = MagicMock()
        self.widget.show_help = MagicMock()
        self.widget.toggle_grid = MagicMock()
        self.widget.pan_view = MagicMock()

        # Simulate key presses and check calls
        self.widget.keyPressEvent(MagicMock(key=lambda: Qt.Key_R))
        self.widget.reset_zoom.assert_called_once()

        self.widget.keyPressEvent(MagicMock(key=lambda: Qt.Key_S))
        self.widget.save_figure.assert_called_once()

        self.widget.keyPressEvent(MagicMock(key=lambda: Qt.Key_H))
        self.widget.show_help.assert_called_once()

        self.widget.keyPressEvent(MagicMock(key=lambda: Qt.Key_T))
        self.widget.toggle_grid.assert_called_once()

        self.widget.keyPressEvent(MagicMock(key=lambda: Qt.Key_Up))
        self.widget.pan_view.assert_called_with(0, 10)

        self.widget.keyPressEvent(MagicMock(key=lambda: Qt.Key_Down))
        self.widget.pan_view.assert_called_with(0, -10)

        self.widget.keyPressEvent(MagicMock(key=lambda: Qt.Key_Left))
        self.widget.pan_view.assert_called_with(-1, 0)

        self.widget.keyPressEvent(MagicMock(key=lambda: Qt.Key_Right))
        self.widget.pan_view.assert_called_with(1, 0)


    @patch("FinalProject.assets.graph_widget.show_message")
    def test_show_help(self, mock_show_message: MagicMock) -> None:
        """
        Test that the help text is displayed correctly.
        """
        self.widget.show_help()
        mock_show_message.assert_called_once() # Verify the help message is shown
        args: tuple = mock_show_message.call_args[0]
        # Verify the title is "Help"
        self.assertEqual(args[1], "Help")
        # Verify the help text contains the expected content
        self.assertIn("Graph Widget Help", args[2])


    def test_on_click_valid(self) -> None:
        """
        Test valid mouse click handling.
        """
        mock_event: MagicMock = MagicMock(button=1, inaxes=True, xdata=100, ydata=200)
        self.widget.on_click(mock_event)
        self.assertTrue(self.widget._dragging) # Verify dragging mode is enabled
        self.assertEqual(self.widget._last_x, 100) # Verify the last x-coordinate is updated
        self.assertEqual(self.widget._last_y, 200) # Verify the last y-coordinate is updated


    def test_on_click_invalid(self) -> None:
        """
        Test invalid mouse click handling (e.g., click outside axes).
        """
        mock_event: MagicMock = MagicMock(button=2, inaxes=False)
        self.widget.on_click(mock_event)
        self.assertFalse(self.widget._dragging) # Dragging should not be enabled


    def test_on_release(self) -> None:
        """
        Test mouse release handling.
        """
        mock_event: MagicMock = MagicMock(button=1)
        self.widget._dragging = True
        self.widget.on_release(mock_event)
        self.assertFalse(self.widget._dragging) # Verify dragging mode is disabled


    def test_on_move(self) -> None:
        """
        Test mouse movement handling for panning.
        """
        mock_axes: MagicMock = MagicMock()
        mock_axes.get_xlim.return_value = (0, 10)
        mock_axes.get_ylim.return_value = (0, 10)

        self.widget._dragging = True
        self.widget._last_x = 5
        self.widget._last_y = 5

        mock_event: MagicMock = MagicMock(inaxes=mock_axes, xdata=6, ydata=7)
        self.widget.on_move(mock_event)

        # Verify axes are updated with the correct limits
        mock_axes.set_xlim.assert_called_once_with(-1, 9)
        mock_axes.set_ylim.assert_called_once_with(-2, 8)


    def test_reset_zoom(self) -> None:
        """
        Test that the zoom is reset correctly.
        """
        mock_axes: MagicMock = MagicMock()
        self.widget.figure.gca = MagicMock(return_value=mock_axes)

        self.widget.reset_zoom()
        mock_axes.autoscale.assert_called_once() # Verify autoscaling is triggered


    def test_toggle_grid(self) -> None:
        """
        Test grid toggling functionality.
        """
        mock_axes: MagicMock = MagicMock()
        self.widget.figure.gca = MagicMock(return_value=mock_axes)
        mock_axes._axisbelow = False

        self.widget.toggle_grid()
        mock_axes.grid.assert_called_once_with(True) # Verify grid is toggled on


    @patch("PySide6.QtWidgets.QFileDialog.getSaveFileName")
    def test_save_figure(self, mock_get_save_file_name: MagicMock) -> None:
        """
        Test that the save figure functionality works as expected.
        """
        mock_get_save_file_name.return_value = ("test.png", None)
        self.widget.figure.savefig = MagicMock()

        self.widget.save_figure()
        self.widget.figure.savefig.assert_called_once_with("test.png") # Verify the figure is saved


    @patch("PySide6.QtWidgets.QFileDialog.getSaveFileName")
    def test_save_figure_cancel(self, mock_get_save_file_name: MagicMock) -> None:
        """
        Test that saving a figure does nothing when cancelled.
        """
        mock_get_save_file_name.return_value = ("", None)
        self.widget.figure.savefig = MagicMock()

        self.widget.save_figure()
        # Verify no file is saved if the dialog is cancelled
        self.widget.figure.savefig.assert_not_called()


if __name__ == "__main__":
    unittest.main()
