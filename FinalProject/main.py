# Standard library imports
import sys

# Third-party imports
from PySide6.QtWidgets import QApplication

# Local project-specific imports
from windows.main_window import MainWindow


def main():
    """
    Initializes and runs the application. Includes error handling for initialization
    and window setup processes.
    """
    try:
        # Try to create and run the application
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()  # Display the main window on the screen
        sys.exit(app.exec())  # Ensures the program exits cleanly after closing
    except Exception as e:
        # Catch any exception that occurs during the application startup
        print(f"❌ [ERROR] An error occurred while initializing the application: {e}")
        # Provide additional information for the error
        print("⚠️ [WARNING] The application encountered an issue and will now exit.")
        sys.exit(1)  # Exit the program with an error code


# Check if the script is being run as the main program
if __name__ == "__main__":
    main()