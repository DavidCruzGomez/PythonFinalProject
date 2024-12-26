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
FinalProject/
├── assets/
│   ├── users_db.json             # User database
│   ├── email_config.json         # Email configuration (SMTP)
│   ├── regex.py                  # Regular expressions (e.g., for validating emails)
│   └── utils.py                  # Utility functions (e.g., displaying messages)
├── styles/
│   ├── styles.py                 # Styles for the GUI (buttons, text fields, etc.)
│   └── __init__.py               # Empty file to import the styles module
├── windows/
│   ├── main_window.py            # Main window for login
│   ├── dashboard_window.py       # User dashboard window
│   ├── registration_window.py    # User registration window
│   ├── recovery_window.py        # Password recovery window
│   └── __init__.py               # Empty file to import the windows module
├── requirements.txt              # Project dependencies
├── main.py                       # Main file to run the application
└── README.md                     # This file