"""
Unit tests for user database management functions.

This test suite contains unit tests for various functions related to managing
the user database in the application. The tests ensure the correct functionality
of operations such as loading, saving, validating, and adding users to the database,
as well as retrieving user information based on different attributes (username and email).

Key tests include:

- `test_load_users_db_file_not_found`: Verifies that the users database returns an empty dictionary
if the file does not exist.

- `test_load_users_db_success`: Ensures that the users database is loaded correctly when the file
contains valid JSON data.

- `test_load_users_db_invalid_json`: Simulates and tests the handling of
invalid JSON in the database file.

- `test_validate_users_db_valid`: Ensures that a well-structured users database passes validation.

- `test_validate_users_db_missing_fields`: Verifies that the validation function raises an error
when required fields are missing in the database.

- `test_save_users_db`: Ensures the users database can be saved correctly without errors.

- `test_add_user_to_db`: Verifies the successful addition of a new user to the database.

- `test_add_user_to_db_existing_user`: Ensures that attempting to add a user
with an existing username raises a validation error.

- `test_get_user_by_username`: Verifies that the correct user is retrieved by username.

- `test_get_user_by_email`: Verifies that the correct user is retrieved by email.

- `test_check_password_hash`: Ensures the correct verification of passwords against stored hashes.

- `test_username_exists`: Verifies that the system correctly identifies
whether a username exists in the database.

The tests use Python's `unittest` framework, along with mocking techniques,
to simulate various scenarios such as loading data from a file,
validating data structure, and handling errors, without the need
for a real database or filesystem operations.
"""

# Standard library imports
import json
import unittest
from unittest.mock import patch, mock_open

# Third-party imports
import bcrypt

# Local imports
from FinalProject.assets.custom_errors import DatabaseError, ValidationError
from FinalProject.assets.users_db import (
    validate_users_db, load_users_db, save_users_db, add_user_to_db,
    get_user_by_username, get_user_by_email, check_password_hash, username_exists
)


class TestUsersDb(unittest.TestCase):
    """
    Test suite for testing user database management functions.

    This class contains unit tests for functions related to loading, saving, and validating
    a simulated users database, as well as adding new users, checking credentials, and verifying
    the existence of users in the database.
    """

    # Mocks the check for whether the database file exists
    # and simulates opening an empty file to test if it is handled correctly
    @patch("FinalProject.assets.users_db.os.path.exists")
    @patch("FinalProject.assets.users_db.open", new_callable=mock_open, read_data='{}')
    def test_load_users_db_file_not_found(self, mock_open, mock_exists):
        """
        Test case for loading users database when the file does not exist.

        This test simulates the scenario where the users database file is not found,
        and checks that the function correctly returns an empty dictionary.
        """
        mock_exists.return_value = False # Simulating that the file doesn't exist
        users = load_users_db()
        self.assertEqual(users, {}) # Verifying that the loaded database is empty


    # Mocks opening a file with an empty users database to test successful loading
    @patch("FinalProject.assets.users_db.open", new_callable=mock_open, read_data='{}')
    def test_load_users_db_success(self, mock_open):
        """
        Test case for successfully loading the user´s database.

        This test ensures that the users database is loaded correctly when the file exists
        and contains valid JSON data.
        """
        users = load_users_db()
        self.assertEqual(users, {}) # Verifying that the loaded database is empty


    # Mocks loading data with invalid JSON to test error handling
    @patch("FinalProject.assets.users_db.open", new_callable=mock_open)
    @patch("FinalProject.assets.users_db.json.load")
    def test_load_users_db_invalid_json(self, mock_json_load, mock_open):
        """
        Test case for handling invalid JSON in the users database file.

        This test simulates the scenario where the JSON in the users database file is malformed,
        and checks that the function handles this error and returns an empty dictionary.
        """
        # Simulating a JSON error
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)

        result = load_users_db()
        self.assertEqual(result, {}) # Verify error handling by returning an empty dictionary


    # Mocks validating a correctly structured users database
    @patch("FinalProject.assets.users_db.open", new_callable=mock_open)
    @patch("FinalProject.assets.users_db.json.load",
           return_value={"user": {"email": "test@example.com"}})
    def test_validate_users_db_valid(self, mock_json_load, mock_open):
        """
        Test case for validating a correctly structured user´s database.

        This test ensures that the `validate_users_db` function correctly validates the structure
        of the loaded database when all required fields are present.
        """
        result = validate_users_db({"user": {"email": "test@example.com", "password_hash": "hash"}})
        self.assertTrue(result) # Verifying that the database is validated correctly


    # Mocks validating a database with missing fields
    @patch("FinalProject.assets.users_db.open", new_callable=mock_open)
    @patch("FinalProject.assets.users_db.json.load")
    def test_validate_users_db_missing_fields(self, mock_json_load, mock_open):
        """
        Test case for invalid users database with missing required fields.

        This test ensures that the `validate_users_db` function raises a `DatabaseError`
        when required fields (e.g., password_hash) are missing from a user entry.
        """
        # Verifying that a DatabaseError is raised if fields are missing
        with self.assertRaises(DatabaseError):
            validate_users_db({"user": {"email": "test@example.com"}})


    # Mocks the function to save the users database
    @patch("FinalProject.assets.users_db.open", new_callable=mock_open)
    def test_save_users_db(self, mock_open):
        """
        Test case for saving the user´s database.

        This test ensures that the `save_users_db` function works correctly and does not raise
        a `DatabaseError` when saving a valid user´s database.
        """
        try:
            save_users_db({"user": {"email": "test@example.com", "password_hash": "hash"}})
        except DatabaseError:
            # Verifying that no error is raised
            self.fail("save_users_db() raised DatabaseError unexpectedly!")


    # Mocks adding a new user to the database
    @patch("FinalProject.assets.users_db.load_users_db", return_value={})
    @patch("FinalProject.assets.users_db.save_users_db")
    def test_add_user_to_db(self, mock_save_users_db, mock_load_users_db):
        """
        Test case for adding a new user to the user´s database.

        This test verifies that a new user is successfully added to the database and the
        `save_users_db` function is called to save the updated database.
        """
        add_user_to_db("newuser", "newuser@example.com", "Password1!")
        mock_save_users_db.assert_called_once() # Verifying that the save function is called once


    # Mocks attempting to add a user with an existing username
    @patch("FinalProject.assets.users_db.load_users_db", return_value={
        "existinguser": {"email": "existinguser@example.com", "password_hash": "hash"}})
    def test_add_user_to_db_existing_user(self, mock_load_users_db):
        """
        Test case for trying to add a user with an existing username.

        This test ensures that the `add_user_to_db` function raises a `ValidationError`
        when attempting to add a new user with a username that already exists in the database.
        """
        # Verifying that a ValidationError is raised if the username exists
        with self.assertRaises(ValidationError):
            add_user_to_db("existinguser", "newemail@example.com", "Password1!")


    # Mocks getting a user by their username
    @patch("FinalProject.assets.users_db.load_users_db",
           return_value={"user": {"email": "user@example.com", "password_hash": "hash"}})
    def test_get_user_by_username(self, mock_load_users_db):
        """
        Test case for retrieving a user by username.

        This test verifies that the `get_user_by_username` function correctly retrieves a user
        when provided with an existing username.
        """
        user = get_user_by_username("user")
        self.assertIsNotNone(user) # Verifying that a user is returned


    # Mocks getting a user by their email address
    @patch("FinalProject.assets.users_db.load_users_db",
           return_value={"user": {"email": "user@example.com", "password_hash": "hash"}})
    def test_get_user_by_email(self, mock_load_users_db):
        """
        Test case for retrieving a user by email.

        This test verifies that the `get_user_by_email` function correctly retrieves a user
        when provided with an existing email address.
        """
        user = get_user_by_email("user@example.com")
        self.assertIsNotNone(user) # Verifying that a user is returned


    # Verifies that the password matches its hash
    def test_check_password_hash(self):
        """
        Test case for checking if a password matches its hash.

        This test ensures that the `check_password_hash` function correctly verifies
        whether a given password matches the stored password hash.
        """
        password = "Password1!"

        # Generating the hash
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Verifying that the password matches the hash
        self.assertTrue(check_password_hash(password_hash, password))


    # Mocks checking if a username already exists in the database
    @patch("FinalProject.assets.users_db.load_users_db",
           return_value={"existinguser": {"email": "existinguser@example.com",
                                          "password_hash": "hash"}})
    def test_username_exists(self, mock_load_users_db):
        """
        Test case for checking if a username exists in the database.

        This test verifies that the `username_exists` function correctly identifies
        whether a username already exists in the user´s database.
        """
        # Verifying that the function returns True if the username exists
        self.assertTrue(username_exists("existinguser"))


if __name__ == '__main__':
    unittest.main()
