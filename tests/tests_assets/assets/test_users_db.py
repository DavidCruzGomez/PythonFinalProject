# Standard library imports
import unittest
from unittest.mock import patch, mock_open
import bcrypt
import json

# Local imports
from FinalProject.assets.users_db import (
    validate_users_db, load_users_db, save_users_db, add_user_to_db,
    get_user_by_username, get_user_by_email, check_password_hash, username_exists
)
from FinalProject.assets.custom_errors import DatabaseError, ValidationError


class TestUsersDb(unittest.TestCase):

    @patch("FinalProject.assets.users_db.os.path.exists")
    @patch("FinalProject.assets.users_db.open", new_callable=mock_open, read_data='{}')
    def test_load_users_db_file_not_found(self, mock_open, mock_exists):
        mock_exists.return_value = False
        users = load_users_db()
        self.assertEqual(users, {})


    @patch("FinalProject.assets.users_db.open", new_callable=mock_open, read_data='{}')
    def test_load_users_db_success(self, mock_open):
        users = load_users_db()
        self.assertEqual(users, {})


    @patch("FinalProject.assets.users_db.open", new_callable=mock_open)
    @patch("FinalProject.assets.users_db.json.load")
    def test_load_users_db_invalid_json(self, mock_json_load, mock_open):
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        result = load_users_db()
        self.assertEqual(result, {})


    @patch("FinalProject.assets.users_db.open", new_callable=mock_open)
    @patch("FinalProject.assets.users_db.json.load",
           return_value={"user": {"email": "test@example.com"}})
    def test_validate_users_db_valid(self, mock_json_load, mock_open):
        result = validate_users_db({"user": {"email": "test@example.com", "password_hash": "hash"}})
        self.assertTrue(result)


    @patch("FinalProject.assets.users_db.open", new_callable=mock_open)
    @patch("FinalProject.assets.users_db.json.load")
    def test_validate_users_db_missing_fields(self, mock_json_load, mock_open):
        with self.assertRaises(DatabaseError):
            validate_users_db({"user": {"email": "test@example.com"}})


    @patch("FinalProject.assets.users_db.open", new_callable=mock_open)
    def test_save_users_db(self, mock_open):
        try:
            save_users_db({"user": {"email": "test@example.com", "password_hash": "hash"}})
        except DatabaseError:
            self.fail("save_users_db() raised DatabaseError unexpectedly!")


    @patch("FinalProject.assets.users_db.load_users_db", return_value={})
    @patch("FinalProject.assets.users_db.save_users_db")
    def test_add_user_to_db(self, mock_save_users_db, mock_load_users_db):
        add_user_to_db("newuser", "newuser@example.com", "Password1!")
        mock_save_users_db.assert_called_once()


    @patch("FinalProject.assets.users_db.load_users_db", return_value={
        "existinguser": {"email": "existinguser@example.com", "password_hash": "hash"}})
    def test_add_user_to_db_existing_user(self, mock_load_users_db):
        with self.assertRaises(ValidationError):
            add_user_to_db("existinguser", "newemail@example.com", "Password1!")


    @patch("FinalProject.assets.users_db.load_users_db",
           return_value={"user": {"email": "user@example.com", "password_hash": "hash"}})
    def test_get_user_by_username(self, mock_load_users_db):
        user = get_user_by_username("user")
        self.assertIsNotNone(user)


    @patch("FinalProject.assets.users_db.load_users_db",
           return_value={"user": {"email": "user@example.com", "password_hash": "hash"}})
    def test_get_user_by_email(self, mock_load_users_db):
        user = get_user_by_email("user@example.com")
        self.assertIsNotNone(user)


    def test_check_password_hash(self):
        password = "Password1!"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.assertTrue(check_password_hash(password_hash, password))


    @patch("FinalProject.assets.users_db.load_users_db",
           return_value={"existinguser": {"email": "existinguser@example.com",
                                          "password_hash": "hash"}})
    def test_username_exists(self, mock_load_users_db):
        self.assertTrue(username_exists("existinguser"))


if __name__ == '__main__':
    unittest.main()
