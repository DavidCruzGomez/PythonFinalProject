"""
Interactive Graph Widget for PySide6 with Matplotlib.

This module defines the `GraphWidget` class, which provides an interactive graph
display built on PySide6 and Matplotlib. The widget enables users to interact
with the graph through mouse and keyboard inputs, offering features like zooming,
panning, grid toggling, and saving graphs.

Key Features:
-------------
1. **Mouse Interactions**:
   - Left-click to display the X and Y positions at the mouse location.
   - Drag to pan the graph.
   - Scroll to zoom in and out of the graph.

2. **Keyboard Shortcuts**:
   - `R`: Reset the zoom to the full data area.
   - `S`: Save the current graph as an image.
   - `T`: Toggle grid visibility.
   - Arrow keys (`Up`, `Down`, `Left`, `Right`): Pan the graph in the respective direction.
   - `H`: Display a help dialog with instructions for interacting with the graph.

3. **Customizable Events**:
   - `on_click`: Handles mouse click events.
   - `on_release`: Detects mouse button release.
   - `on_move`: Enables panning via mouse drag.
   - `on_scroll`: Implements zoom functionality centered on the cursor.

4. **Other Utilities**:
   - `reset_zoom`: Restores the graph view to the full data range.
   - `toggle_grid`: Shows or hides the grid on the graph.
   - `save_figure`: Opens a dialog to save the current graph in various formats
    (PNG, JPG, PDF, etc.).
"""
# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QSizePolicy, QFileDialog, QInputDialog)
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Local project-specific imports
from src.assets.utils import show_message


class GraphWidget(FigureCanvas):
    """
    Custom widget for displaying and interacting with matplotlib graphs
    within a Qt application. This class provides functionality for panning,
    zooming, toggling grid visibility, saving graphs, and displaying help instructions.
    """

    def __init__(self, fig) -> None:
        """
        Initialize the GraphWidget with a matplotlib figure.

        Args:
            fig (matplotlib.figure.Figure): The matplotlib figure to display.
        """
        # Call the base constructor of FigureCanvas with the figure
        super().__init__(fig)

        # Configure the size and geometry of the widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

        # Enable focus for keyboard interaction
        self.setFocusPolicy(Qt.StrongFocus)  # Make the canvas interactive
        self.setFocus()  # Make it receive keyboard events

        # Variables for panning
        self._dragging: bool = False
        self._last_x: float | None = None
        self._last_y: float | None = None
        self._annotations: dict = {}

        # Connect mouse events for click, release, and movement
        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('motion_notify_event', self.on_move)
        self.mpl_connect('scroll_event', self.on_scroll)

        print("🔍 [DEBUG] GraphWidget initialized.")

    def keyPressEvent(self, event) -> None:
        """
        Handle keyboard events to enable shortcuts for interacting with the graph.

        Supported shortcuts:
        - R: Reset zoom
        - S: Save the graph as an image
        - H: Show help instructions
        - T: Toggle grid visibility
        - Arrow keys: Pan the graph (Up, Down, Left, Right)
        - A: Add an annotation to the graph
        - D: Delete the last added annotation
        - L: Toggle the visibility of the graph legend
        """
        if event.key() == Qt.Key_R:  # Reset view
            self.reset_zoom()
            print("🔄 [INFO] Zoom reset to the full area.")

        elif event.key() == Qt.Key_S:  # Save graph
            self.save_figure()
            print("💾 [SUCCESS] Graph saved as an image.")

        elif event.key() == Qt.Key_H:  # Show help
            self.show_help()
            print("❓ [HELP] Showing help.")

        elif event.key() == Qt.Key_T:  # Toggle grid visibility
            self.toggle_grid()
            print("🔲 [TOGGLE] Toggling grid visibility.")

        elif event.key() == Qt.Key_Up:  # Pan graph up
            self.pan_view(0, 10)
            print("⬆️ [MOVE] Panned up.")

        elif event.key() == Qt.Key_Down:  # Pan graph down
            self.pan_view(0, -10)
            print("⬇️ [MOVE] Panned down.")

        elif event.key() == Qt.Key_Left:  # Pan graph left
            self.pan_view(-1, 0)
            print("⬅️ [MOVE] Panned left.")

        elif event.key() == Qt.Key_Right:  # Pan graph right
            self.pan_view(1, 0)
            print("➡️ [MOVE] Panned right.")

        elif event.key() == Qt.Key_A:  # Add annotation
            self.add_annotation()

        elif event.key() == Qt.Key_D:  # Delete last annotation
            self.delete_last_annotation()

        elif event.key() == Qt.Key_L:  # Toggle legend
            self.toggle_legend()


    def show_help(self) -> None:
        """
        Display a help dialog showing keyboard shortcuts and instructions
        for interacting with the graph widget.
        """
        help_text: str = """
        Graph Widget Help:

        - Use the arrow keys (Up, Down, Left, Right) to pan the graph.
        - Use scroll to zoom in and out.
        - Press 'R' to reset the zoom to the full data area.
        - Press 'S' to save the current graph as an image.
        - Press 'T' to toggle the grid visibility.
        - Press 'A' to add annotation
        - Press 'D' to delete last annotation
        - Press 'L' to Toggle legend
        - Click on the graph to see the X and Y positions at the mouse location.
        - Drag the mouse to pan the graph.

        To save the graph, press 'S' and choose the file format.
        """

        # Print the help text to the console
        print(help_text)

        # Use the show_message function to display the help content
        show_message(self, "Help", help_text)

    def on_click(self, event: MouseEvent) -> None:
        """
        Handle mouse click events on the graph. Displays the X and Y
        coordinates of the click position if it occurs within the plot area.

        Args:
            event: The mouse event containing the click information.
        """
        try:
            if event.button == 1 and event.inaxes:  # Left mouse button and within axes
                self._dragging = True
                # Get the X position where the click occurred
                self._last_x = event.xdata
                # Get the Y value corresponding to the X position
                self._last_y = event.ydata

                if self._last_x is not None and self._last_y is not None:
                    print(f"🖱️ [CLICK] Click detected at X: {self._last_x}, Y: {self._last_y}.")
                else:
                    print("🖱️ [CLICK] Click occurred outside of the data range.")
            else:
                print("⚠️ [WARNING] Invalid click. It might be outside of the plot"
                      " or the wrong mouse button was used.")

        except AttributeError as atr_err:
            print(f"❌ [ERROR] An error occurred with the event attributes: {atr_err}")

        except Exception as gen_err:
            print(f"❌ [ERROR] An unexpected error occurred: {gen_err}")

    def on_release(self, event: MouseEvent) -> None:
        """
        Handle mouse release events to stop panning.

        Args:
            event: The mouse release event.
        """
        try:
            if event.button == 1:  # Left mouse button
                self._dragging = False
        except AttributeError as atr_err:
            print(f"❌ [ERROR] An error occurred with the event attributes: {atr_err}")

        except Exception as gen_err:
            print(f"❌ [ERROR] An unexpected error occurred: {gen_err}")

    def on_move(self, event: MouseEvent) -> None:
        """
        Handle mouse movement events for panning the graph when dragging.

        Args:
            event: The mouse move event.
        """
        try:
            if self._dragging and event.inaxes:
                dx: float = event.xdata - self._last_x
                dy: float = event.ydata - self._last_y

                # Move the axis limits
                axis = event.inaxes
                xlim = axis.get_xlim()
                ylim = axis.get_ylim()

                # Adjust the axis limits to move the graph
                axis.set_xlim(xlim[0] - dx, xlim[1] - dx)
                axis.set_ylim(ylim[0] - dy, ylim[1] - dy)

                # Update the last mouse position
                self._last_x = event.xdata
                self._last_y = event.ydata

                # Redraw the canvas to reflect the change
                self.draw()

                print(f"🔍 [INFO] Graph panned by dx: {dx}, dy: {dy}.")

        except AttributeError as atr_err:
            print(f"❌ [ERROR] An error occurred with the event attributes: {atr_err}")

        except Exception as gen_err:
            print(f"❌ [ERROR] An unexpected error occurred: {gen_err}")

    def pan_view(self, dx: float, dy: float) -> None:
        """
        Pan the graph by adjusting the axis limits.

        Args:
            dx: Horizontal shift (positive for right, negative for left).
            dy: Vertical shift (positive for up, negative for down).
        """
        # Get the current axes
        axis = self.figure.gca()

        # Get current limits of the axes
        x_min, x_max = axis.get_xlim()
        y_min, y_max = axis.get_ylim()

        # Adjust the axis limits based on the pan direction (dx, dy)
        axis.set_xlim(x_min + dx, x_max + dx)
        axis.set_ylim(y_min + dy, y_max + dy)

        # Redraw the canvas to reflect the change
        self.draw()

    def on_scroll(self, event: MouseEvent) -> None:
        """
        Handle scroll events for zooming in and out on the graph.

        Args:
            event: The mouse scroll event.
        """
        try:
            if event.inaxes:  # Ensure the scroll occurs within the plot area
                axis = event.inaxes
                x_min, x_max = axis.get_xlim()
                y_min, y_max = axis.get_ylim()
                x_range = x_max - x_min
                y_range = y_max - y_min

                # Determine zoom factor (0.9 for zooming in, 1.1 for zooming out)
                zoom_factor: float = 0.9 if event.button == 'up' else 1.1

                # Calculate new limits centered on the cursor
                mouse_x, mouse_y = event.xdata, event.ydata
                new_xlim = [
                    mouse_x - (mouse_x - x_min) * zoom_factor,
                    mouse_x + (x_max - mouse_x) * zoom_factor,
                ]
                new_ylim = [
                    mouse_y - (mouse_y - y_min) * zoom_factor,
                    mouse_y + (y_max - mouse_y) * zoom_factor,
                ]

                # Define zoom bounds (to prevent excessive zooming)
                min_range = 0.02  # Minimum allowable range for both axes
                max_range = 3 * max(x_range, y_range)  # Maximum allowable range

                if (new_xlim[1] - new_xlim[0] < min_range or
                        new_ylim[1] - new_ylim[0] < min_range):
                    print("🔍 [INFO] Zoomed in too far, limit reached.")
                    return
                if (new_xlim[1] - new_xlim[0] > max_range or
                        new_ylim[1] - new_ylim[0] > max_range):
                    print("🔍 [INFO] Zoomed out too far, limit reached.")
                    return

                # Apply the new limits
                axis.set_xlim(new_xlim)
                axis.set_ylim(new_ylim)
                self.draw()

        except AttributeError as atr_err:
            print(f"❌ [ERROR] An error occurred with the event attributes: {atr_err}")
        except Exception as gen_err:
            print(f"❌ [ERROR] An unexpected error occurred: {gen_err}")

    def reset_zoom(self) -> None:
        """Reset the graph zoom to fit the full data area."""
        axis = self.figure.gca()
        axis.autoscale()  # Matplotlib automatically adjust the limits
        self.draw()

    def toggle_grid(self) -> None:
        """Toggle the visibility of the grid on the graph"""
        axis = self.figure.gca()
        current_grid = axis._axisbelow
        axis.grid(not current_grid)  # Toggle the grid state
        axis._axisbelow = not current_grid
        self.draw()  # Redraw the plot


    def add_annotation(self) -> None:
        """Add a text annotation at the clicked position."""
        text, ok = QInputDialog.getText(self, 'Add Annotation', 'Enter annotation text:')
        if ok and text:
            axis = self.figure.gca()
            if self._last_x is not None and self._last_y is not None:
                annotation = axis.annotate(
                    text,
                    xy=(self._last_x, self._last_y),
                    xytext=(10, 10),
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->')
                )
                self._annotations[text] = annotation
                self.draw()
                print(f"📝 [INFO] Added annotation: {text}")


    def delete_last_annotation(self) -> None:
        """Remove the last added annotation."""
        if self._annotations:
            last_key = list(self._annotations.keys())[-1]
            annotation = self._annotations.pop(last_key)
            annotation.remove()
            self.draw()
            print("🗑️ [INFO] Removed last annotation")


    def toggle_legend(self) -> None:
        """Toggle the visibility of the graph legend."""
        axis = self.figure.gca()
        legend = axis.get_legend()
        if legend is None:
            axis.legend()
        else:
            legend.remove()
        self.draw()
        print("📊 [INFO] Toggled legend visibility")


    def save_figure(self) -> None:
        """Open a file dialog to save the current graph as an image file."""
        # Open a file dialog to select the location and file name
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix(".png")  # Default file extension is PNG
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.pdf *.svg)")

        # Show the dialog and capture the selected file path
        file_path, _ = file_dialog.getSaveFileName(self, "Save Graph", "",
                                                   "Images (*.png *.jpg *.jpeg *.pdf *.svg)")

        if file_path:
            try:
                # Save the figure to the selected file path
                self.figure.savefig(file_path)
                print(f"✅ [SUCCESS] Graph saved to: {file_path}")
            except Exception as gen_err:
                print(f"❌ [ERROR] Error saving figure: {gen_err}")
