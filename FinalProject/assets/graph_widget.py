# Standard library imports

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMessageBox,
                               QSizePolicy, QFileDialog)
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# Local project-specific imports


class GraphWidget(FigureCanvas):
    def __init__(self, fig):
        # Call the base constructor of FigureCanvas with the figure
        super().__init__(fig)

        # Configure the size and geometry of the widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        self.setFocusPolicy(Qt.StrongFocus)  # Make the canvas interactive
        self.setFocus()  # Make it receive keyboard events

        # Variables for panning
        self._dragging = False
        self._last_x = None
        self._last_y = None


        # Connect mouse events for click, release, and movement
        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('motion_notify_event', self.on_move)
        self.mpl_connect('scroll_event', self.on_scroll)

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_R:  # Reset view
            self.reset_zoom()
            print("Zoom reset to the full area.")
        elif event.key() == Qt.Key_S:  # Save graph
            self.save_figure()
            print("Graph saved as an image.")

        elif event.key() == Qt.Key_H:  # Show help
            self.show_help()
            print("Showing help.")

        elif event.key() == Qt.Key_T:  # Toggle grid visibility
            self.toggle_grid()
            print("Toggling grid visibility.")

        elif event.key() == Qt.Key_Up:  # Pan up
            self.pan_view(0, 10)  # Move the graph up
            print("Panned up.")

        elif event.key() == Qt.Key_Down:  # Pan down
            self.pan_view(0, -10)  # Move the graph down
            print("Panned down.")

        elif event.key() == Qt.Key_Left:  # Pan left
            self.pan_view(-1, 0)  # Move the graph left
            print("Panned left.")

        elif event.key() == Qt.Key_Right:  # Pan right
            self.pan_view(1, 0)  # Move the graph right
            print("Panned right.")

    def show_help(self):
        """Display a help dialog with keyboard shortcuts and usage instructions."""
        help_text = """
        Graph Widget Help:

        - Use the arrow keys (Up, Down, Left, Right) to pan the graph.
        - Use scroll to zoom in and out.
        - Press 'R' to reset the zoom to the full data area.
        - Press 'S' to save the current graph as an image.
        - Press 'T' to toggle the grid visibility.
        - Click on the graph to see the X and Y positions at the mouse location.
        - Drag the mouse to pan the graph.

        To save the graph, press 'S' and choose the file format.
        """

        # Print the help text to the console
        print(help_text)

        # Create a message box to show the help content
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Help")
        msg_box.setText("Instructions for interacting with the graph:")
        msg_box.setInformativeText(help_text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def on_click(self, event):
        """Detect click on the graph and display the X-axis and Y-axis values."""
        try:
            if event.button == 1 and event.inaxes:
                self._dragging = True
                # Get the X position where the click occurred
                self._last_x = event.xdata
                # Get the Y value corresponding to the X position
                self._last_y = event.ydata

                if self._last_x is not None and self._last_y is not None:
                    print(f"X Position: {self._last_x}, Y Position: {self._last_y}")
                else:
                    print("Click occurred outside of the data range.")
            else:
                print("Invalid click. It might be outside of the plot or the wrong mouse button "
                      "was used.")

        except AttributeError as atr_err:
            print(f"An error occurred with the event attributes: {atr_err}")

        except Exception as gen_err:
            print(f"An unexpected error occurred: {gen_err}")

    def on_release(self, event: MouseEvent):
        """Detect mouse release to stop panning."""
        try:
            if event.button == 1:
                self._dragging = False
        except AttributeError as atr_err:
            print(f"An error occurred with the event attributes: {atr_err}")

        except Exception as gen_err:
            print(f"An unexpected error occurred: {gen_err}")

    def on_move(self, event: MouseEvent):
        """Detect mouse movement to move the graph (pan)."""
        try:
            if self._dragging and event.inaxes:
                dx = event.xdata - self._last_x
                dy = event.ydata - self._last_y

                # Move the axis limits
                ax = event.inaxes
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()

                # Adjust the axis limits to move the graph
                ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
                ax.set_ylim(ylim[0] - dy, ylim[1] - dy)

                # Update the last mouse position
                self._last_x = event.xdata
                self._last_y = event.ydata

                # Redraw the canvas to reflect the change
                self.draw()
        except AttributeError as atr_err:
            print(f"An error occurred with the event attributes: {atr_err}")

        except Exception as gen_err:
            print(f"An unexpected error occurred: {gen_err}")

    def pan_view(self, dx, dy):
        """Move the axes to simulate panning."""
        # Get the current axes
        ax = self.figure.gca()

        # Get current limits of the axes
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        # Adjust the axis limits based on the pan direction (dx, dy)
        ax.set_xlim(x_min + dx, x_max + dx)
        ax.set_ylim(y_min + dy, y_max + dy)

        # Redraw the canvas to reflect the change
        self.draw()

    def on_scroll(self, event: MouseEvent):
        """Handle mouse scroll events for zooming."""
        try:
            if event.inaxes:
                ax = event.inaxes
                x_min, x_max = ax.get_xlim()
                y_min, y_max = ax.get_ylim()
                x_range = x_max - x_min
                y_range = y_max - y_min

                # Determine zoom factor (0.9 for zooming in, 1.1 for zooming out)
                zoom_factor = 0.9 if event.button == 'up' else 1.1

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
                    print("Zoomed in too far, limit reached.")
                    return
                if (new_xlim[1] - new_xlim[0] > max_range or
                        new_ylim[1] - new_ylim[0] > max_range):
                    print("Zoomed out too far, limit reached.")
                    return

                # Apply the new limits
                ax.set_xlim(new_xlim)
                ax.set_ylim(new_ylim)
                self.draw()

        except AttributeError as atr_err:
            print(f"An error occurred with the event attributes: {atr_err}")
        except Exception as gen_err:
            print(f"An unexpected error occurred: {gen_err}")

    def reset_zoom(self):
        """Reset the zoom to display the entire data area."""
        ax = self.figure.gca()
        ax.autoscale()  # Matplotlib automatically adjust the limits
        self.draw()

    def toggle_grid(self):
        """Toggle the visibility of the grid."""
        ax = self.figure.gca()
        current_grid = ax._axisbelow
        ax.grid(not current_grid)  # Toggle the grid state
        ax._axisbelow = not current_grid
        self.draw()  # Redraw the plot

    def save_figure(self):
        """Save the current figure to a file."""
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
                print(f"Graph saved to: {file_path}")
            except Exception as gen_err:
                print(f"Error saving figure: {gen_err}")