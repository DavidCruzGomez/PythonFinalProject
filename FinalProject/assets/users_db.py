# Standard library imports
import json
import os
import re

# Third-party imports
import bcrypt

# Local imports
from FinalProject.assets.regex import EMAIL_REGEX
from FinalProject.assets.custom_errors import DatabaseError, ValidationError, UserNotFoundError


# Path to the file simulating the user's database
DB_FILE = os.path.join(os.getcwd(), "assets", "users_db.json")


def validate_users_db(users_db: dict) -> bool:
    """
    Validates the structure of the user's database.

    Args:
        users_db (dict): The user's database.

    Returns:
        bool: `True` if the database is valid, `False` if it is not.

    Raises:
        DatabaseError: If the database structure is invalid or missing required fields.
    """
    print("⏳ [INFO] Validating the structure of the users database...")
    for username, details in users_db.items():
        # Ensure 'email' and 'password_hash' are present for each user
        if "email" not in details or "password_hash" not in details:
            raise DatabaseError(f"Missing fields for user '{username}': {details}")
        # Validate the email format using regex
        if not re.fullmatch(EMAIL_REGEX, details["email"]):
            raise DatabaseError(f"Invalid email format for user '{username}': "
                                f"{details['email']}")
    print("✅ [SUCCESS] The users database structure is valid.")
    return True  # Return True if all users are valid

def load_users_db() -> dict:
    """
    Load the users database from a JSON file.

    Returns:
        dict: A dictionary with the loaded users, or an empty dictionary if loading fails.

    Raises:
        DatabaseError: If the users database file cannot be found, is not readable,
                       cannot be decoded or is improperly formatted.
    """
    print("⏳ [INFO] Loading users database...")
    # Check if the database file exists
    if not os.path.exists(DB_FILE):
        print("📁 [INFO] Database file not found. Returning an empty user database.")
        return {}

    try:
        with open(DB_FILE, "r", encoding='utf-8') as file:
            data = json.load(file)

            # Validate the structure of the database
            if not validate_users_db(data):
                print("❌ [ERROR] Invalid user database structure.")
                raise DatabaseError("Invalid user database structure.")
            return data

        print("✅ [SUCCESS] Database loaded successfully.")
        return json.load(file)

    except json.JSONDecodeError as e:
        print(f"❌ [ERROR] Failed to decode JSON from the database: {e}")
        raise DatabaseError("Failed to decode JSON from the database.") from e

    except IOError as e:
        print(f"❌ [ERROR] I/O error while loading the database: {e}")
        raise DatabaseError("I/O error while loading the database.") from e

    except Exception as e:
        print(f"❌ [ERROR] Unexpected error in loading database: {e}")
        raise DatabaseError("Unexpected error while loading the database.") from e


def save_users_db(users_db: dict) -> None:
    """
    Save the users database to a JSON file.

    Args:
        users_db (dict): The dictionary of users to save.

    Raises:
        DatabaseError: If there is an issue saving the database.
    """
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True) # Ensure directory exists
        with open(DB_FILE, "w", encoding='utf-8') as file:
            json.dump(users_db, file, indent=4, ensure_ascii=False) # Save with 4 spaces indentation
        print("✅ [SUCCESS] Database saved successfully.")

    except (IOError, json.JSONDecodeError) as e:
        print(f"❌ [ERROR] Failed to save database: {e}")
        raise DatabaseError("Failed to save database.") from e

    except Exception as e:
        print(f"❌ [ERROR] Unexpected error in saving database: {e}")
        raise DatabaseError("Unexpected error while saving the database.") from e


def add_user_to_db(username: str, email: str, password: str) -> None:
    """
    Add a new user to the database.

    This function validates the email and checks whether the username and email are already taken.
    If valid, it hashes the user's password and adds the new user to the database.
    If any validation fails, an error is raised.

    Args:
        username (str): The username.
        email (str): The user's email address.
        password (str): The user's password (hashed before saving).

    Raises:
        ValidationError: If the email format is invalid or the username/email already exists.
        DatabaseError: If there is an issue saving the database or interacting with it.
    """
    email = email.strip().lower()

    # Validate the email format using the regex
    if not re.fullmatch(EMAIL_REGEX, email):
        print(f"❌ [ERROR] Invalid email format: '{email}'")
        raise ValueError(f"Invalid email format: {email}")

    try:
        users_db = load_users_db()

        if username in users_db:
            print(f"❌ [ERROR] Username '{username}' already exists.")
            raise ValueError(f"Username '{username}' already exists.")

        if any(user_data["email"] == email for user_data in users_db.values()):
            print(f"❌ [ERROR] Email '{email}' already exists.")
            raise ValueError(f"Email '{email}' already exists.")

        # Create a password hash using bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Add the new user to the dictionary
        users_db[username] = {
            "email": email,
            "password_hash": password_hash.decode('utf-8')  # Store the hash as a string
        }

        # Save changes to the file
        save_users_db(users_db)
        print(f"✅ [SUCCESS] 👤 User '{username}' added successfully.")

    except ValidationError as ve:
        print(f"❌ [ERROR] Validation error: {ve}")
        raise ve

    except DatabaseError as de:
        print(f"❌ [ERROR] Database error: {de}")
        raise de

    except Exception as e:
        print(f"❌ [ERROR] Unexpected error: {e}")
        raise

def get_user_by_username(username: str) -> dict | None:
    """
    Get the data of a user by their username.

    Args:
        username (str): The username.

    Returns:
        dict | None: The user's data, or None if not found.

    Raises:
        DatabaseError: If there is an issue accessing the database.
    """
    try:
        users_db = load_users_db()
        if users_db.get(username):
            print(f"✅ [INFO] User '{username}' found.")
        else:
            print(f"❌ [ERROR] User '{username}' not found.")
        return users_db.get(username)


    except DatabaseError as e:
        print(f"❌ [ERROR] Database error: {e}")
        return None

    except Exception as e:
        print(f"❌ [ERROR] Unexpected error: {e}")
        return None

def get_user_by_email(email: str) -> dict | None:
    """
    Get the data of a user by their email.

    Args:
        email (str): The email address to search for.

    Returns:
        dict | None: The user's data, or None if not found.

    Raises:
        DatabaseError: If there is an issue accessing the database.
        UserNotFoundError: If no user is found with the given email address.
    """
    try:
        # Validate the email format using the regex
        if not re.fullmatch(EMAIL_REGEX, email):
            print(f"❌ [ERROR] Invalid email format: '{email}'")
            return None

        users_db = load_users_db()
        for username, details in users_db.items():
            if details.get("email").strip().lower() == email.strip().lower():
                print(f"🔍 [INFO] User '{username}' found with email {email}.")
                return details

        print(f"❌ [ERROR] No user found with email '{email}'.")
        raise UserNotFoundError(email)


    except DatabaseError as e:
        print(f"❌ [ERROR] Database error: {e}")
        return None

    except Exception as e:
        print(f"❌ [ERROR] Unexpected error: {e}")
        return None

def check_password_hash(stored_hash: str, password: str) -> bool:
    """
    Verify if an entered password matches the stored hash.

    Args:
        stored_hash (str): The stored password hash in the database.
        password (str): The password entered by the user.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    try:
        match = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        if match:
            print("✅ [SUCCESS] Password match successful.")
        else:
            print("❌ [ERROR] Password mismatch.")

        return match

    except Exception as e:
        print(f"❌ [ERROR] Error checking password hash: {e}")
        return False

def username_exists(username: str) -> bool:
    """
    Check if a username already exists in the database.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    try:
        exists = get_user_by_username(username) is not None
        if exists:
            print(f"✅ [INFO] Username '{username}' already exists.")
        else:
            print(f"❌ [ERROR] Username '{username}' does not exist.")
        return exists

    except Exception as e:
        print(f"❌ [ERROR] Error checking if username exists: {e}")
        return False
