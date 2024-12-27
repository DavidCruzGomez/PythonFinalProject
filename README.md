# Impulse Buying Factors on TikTok Shop

This is a Final Project created by David Cruz Gómez.
The application is a simulation of a login system, user registration, and password recovery
for an online shopping platform, like TikTok Shop. The interface is developed with PySide6
(a Python interface for Qt), which is a library for creating graphical user interfaces (GUI).

### Main Features:
- **Login**: Users can log in with a username and password.
- **User Registration**: Users can register by creating a new account.
- **Password Recovery**: Users can recover their password via email.
- **Dashboard**: After logging in, users are redirected to a welcome dashboard.

## Technologies Used:
- **PySide6**: For creating the graphical user interface (GUI).
- **JSON**: To store the user database and configurations.
- **bcrypt**: For hashing and verifying user passwords.
- **smtplib**: To send password recovery emails.



## Directory Structure

```plaintext
.
├── FinalProject/
│   ├── assets/
│   │   ├── custom_errors.py            # Custom error classes
│   │   ├── email_cofig.json            # Email configuration (SMTP)
│   │   ├── regex.py                    # Regular expressions (e.g., for validating emails)
│   │   ├── users_db.json               # User database
│   │   ├── users_db.py                 # User database functions
│   │   ├── utils.py                    # Utility functions (e.g., displaying messages)
│   │   └── __init__.py                 # Empty file to import the assets module
│   ├── styles/
│   │   ├── styles.py                   # Styles for the GUI (buttons, text fields, etc.)
│   │   └── __init__.py                 # Empty file to import the styles module
│   ├── windows/
│   │   ├── main_window.py              # Main window for login
│   │   ├── dashboard_window.py         # User dashboard window
│   │   ├── registration_window.py      # User registration window
│   │   ├── recovery_window.py          # Password recovery window
│   │   └── __init__.py                 # Empty file to import the windows module
│   ├── main.py                         # Main file to run the application
│   └── __init__.py                     # Empty file to import the main package
├── tests/
│   ├── tests_assets/
│   │   ├── test_custom_errors.py       # Tests for custom errors
│   │   ├── test_email_config.py        # Tests for email configuration
│   │   ├── test_regex.py               # Tests for regular expressions
│   │   ├── test_users_db.py            # Tests for user database functions
│   │   ├── test_utils.py               # Tests for utility functions
│   │   └── __init__.py                 # Empty file to import the tests_assets module
│   ├── tests_styles/
│   │   ├── test_styles.py              
│   │   └── __init__.py                 # Empty file to import the tests_styles module
│   └── __init__.py                     # Empty file to import the tests package
│ 
├── CHANGELOG.md                        # Project change log
├── LICENSE.md                          # License for the project
├── README.md                           # This file
├── requeriments.txt                    # Project dependencies
├── requeriments_dev.txt                # Development dependencies
├── setup.cfg                           # Configuration for packaging the project
├── setup.py                            # Script to install the project
├── VERSION.txt                         # Current version of the project
└── Dockerfile                          # Docker configuration for the project
