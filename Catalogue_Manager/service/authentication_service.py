from util.db_get_connection import get_connection
from exceptions.exceptions import AuthenticationError

class AuthenticationService:
    def authenticate(self, username: str, password: str):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Query the user
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        # Validate credentials
        if result is None:
            raise AuthenticationError("User not found.")
        
        stored_password = result[0]
        if stored_password != password:
            raise AuthenticationError("Invalid password.")

        return True  # Authenticated successfully
