from flask_login import UserMixin
from app.db_manager import fetchone
from werkzeug.security import check_password_hash
from app.__init__ import db


class User(UserMixin):

    def __init__(self, user_id, password, name, address, role, phoneNum):
        self.user_id = user_id
        self.password = password
        self.name = name
        self.address = address
        self.role = role
        # self.phoneNumber = phoneNum

    @staticmethod
    def findMatchOR(keys, values):
        # Build the SQL query
        sql = "SELECT `user_id`, `password`, `name`, `address`, `role` FROM Users WHERE "
        # Ensure each key gets a placeholder
        where = ' OR '.join([f"`{key}` = %s" for key in keys])
        query = sql + where
        print(f"Executing SQL: {query}")
        # Execute the query and fetch one result
        result = fetchone(query, tuple(values))

        # If no result is found, return None
        if not result:
            return None
        # Unpack the result into the User constructor
        return User(*result)

    @staticmethod
    def verify_password(stored_password, provided_password):
        # Compare the hashed password with the provided one
        return check_password_hash(stored_password, provided_password)
