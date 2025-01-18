# Impulse Buying Factors on TikTok Shop

This is a Final Project created by David Cruz Gómez.
Project Description: This project, is an application that simulates
a login system, user registration, and password recovery for a data
analysis platform like TikTok Shop. In addition to user management,
it provides tools to upload, preprocess, and analyze data related
to impulse buying factors. The interface is developed using PySide6,
ensuring an interactive and functional graphical experience.

## Project Features:

### User Management:
- **Registration**: Allows users to create an account by providing basic information.
- **Login**: Secure access to the system using credentials.
- **Password Recovery**: Offers a process to recover passwords in case of loss.

### Data Analysis Interface:
- **Data Preview**: Displays a quick preview of the DataFrame related to impulse buying factors.
- **Descriptive Statistics**: Provides a statistical summary (mean, median, standard deviation, etc.).
- **Data Download**: Users can download the data file if it's not already available.
- **Data Preprocessing**: Tools for cleaning the DataFrame (handling missing values, removing duplicates, etc.).

### Graph Visualization:
- **Customizable Graphs**: Create customizable graphs based on the DataFrame.
- **Graph Exporting**: Users can save the generated graphs in formats like PNG or JPG.

## Technologies Used:
- **PySide6**: For creating the graphical user interface (GUI).
- **JSON**: To store the user database and configurations.
- **bcrypt**: For hashing and verifying user passwords.
- **smtplib**: To send password recovery emails.
- **pandas**: For data manipulation and analysis.
- **matplotlib**: For generating customizable visualizations (graphs).
- **seaborn**: For enhanced data visualization and statistical graphics.
- **PyQt6**: Alternative Qt framework used in conjunction with PySide6 for GUI elements.
- **openpyxl**: To read and write Excel files, enabling data import/export functionality.
- **selenium**: For automating web browser interactions (download the data from web).



## Directory Structure

```plaintext
.
├── FinalProject/
│   ├── assets/
│   │   ├── exported_graphs/                # Directory for exported graphs
│   │   ├── impulse_buying_data/
│   │   │   ├── cleaned_data.csv            # Cleaned data CSV file
│   │   │   ├── data_dictionary.py          # Data dictionary script
│   │   │   ├── processed_data.csv          # Processed data CSV file
│   │   │   ├── Questionnaire.pdf           # Questionnaire in PDF format
│   │   │   └── Raw_data.xlsx               # Raw data in Excel format
│   │   ├── custom_errors.py                # Custom error classes
│   │   ├── dashboard_window_setup.py       # Dashboard window setup script
│   │   ├── download_files.py               # Script for downloading files
│   │   ├── email_config.json               # Email configuration (SMTP)
│   │   ├── graph_widget.py                 # Graph widget script
│   │   ├── graphics.py                     # Graphics related functions
│   │   ├── preprocess.py                   # Data preprocessing script                    
    │   │   ├── regex.py                    # Regular expressions (e.g., for validating emails)
│   │   ├── UMLDiagram.xml                  # UML Diagram in XML format
│   │   ├── users_db.json                   # User database
│   │   ├── users_db.py                     # User database functions
│   │   ├── utils.py                        # Utility functions (e.g., displaying messages)
│   │   └── __init__.py                     # Empty file to import the assets module
│   ├── styles/
│   │   ├── styles.py                       # Styles for the GUI (buttons, text fields, etc.)
│   │   └── __init__.py                     # Empty file to import the styles module
│   ├── windows/
│   │   ├── main_window.py                  # Main window for login
│   │   ├── dashboard_window.py             # User dashboard window
│   │   ├── registration_window.py          # User registration window
│   │   ├── recovery_window.py              # Password recovery window
│   │   └── __init__.py                     # Empty file to import the windows module
│   ├── main.py                             # Main file to run the application
│   └── __init__.py                         # Empty file to import the main package
├── tests/
│   ├── tests_assets/
│   │   ├── test_custom_errors.py           # Tests for custom errors
│   │   ├── test_dashboard_window_setup.py  # Tests for dashboard window setup      
│   │   ├── test_download_files.py          # Tests for file download functionality
│   │   ├── test_email_config.py            # Tests for email configuration
│   │   ├── test_graph_widget.py            # Tests for graph widget functionality
│   │   ├── test_graphics.py                # Tests for graphics related functions
│   │   ├── test_preprocess.py              # Tests for data preprocessing
│   │   ├── test_regex.py                   # Tests for regular expressions
│   │   ├── test_users_db.py                # Tests for user database functions
│   │   ├── test_utils.py                   # Tests for utility functions
│   │   └── __init__.py                     # Empty file to import the tests_assets module
│   ├── tests_styles/
│   │   ├── test_styles.py                  # Tests for the styles in `styles.py`
│   │   └── __init__.py                     # Empty file to import the tests_styles module
│   ├── tests_windows/
│   │   ├── test_dashboard_window.py        # Tests for the `dashboard_window.py`     
│   │   ├── test_main_window.py             # Tests for the `main_window.py` (login window)
│   │   ├── test_recovery_window.py         # Tests for the `recovery_window.py` (password recovery window)
│   │   ├── test_registration_window.py     # Tests for the `registration_window.py` (user registration window)         
│   │   └── __init__.py                     # Empty file to import the tests_windows module
│   └── __init__.py                         # Empty file to import the tests package
│ 
├── CHANGELOG.md                            # Project change log
├── LICENSE.md                              # License for the project
├── README.md                               # This file
├── requeriments.txt                        # Project dependencies
├── requeriments_dev.txt                    # Development dependencies
├── setup.cfg                               # Configuration for packaging the project
├── setup.py                                # Script to install the project
├── VERSION.txt                             # Current version of the project
└── Dockerfile                              # Docker configuration for the project
```

### Owner
- David Cruz Gómez <david97torrejon@alumnos.cei.es>