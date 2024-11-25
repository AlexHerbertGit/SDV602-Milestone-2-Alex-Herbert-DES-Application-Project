"""JsnDropClient Class"""
import requests

class JsnDropClient:
    def __init__(self, token):
        self.base_url = "https://newsimland.com/~todd/JSON/#"
        self.headers = {"Authorization": f"Bearer {token}"}

    def create_user(self, username, password):
        """Create a new user in the JsnDrop database"""
        data = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/users", headers=self.headers, json=data)
        if response.status_code == 201:
            return True
        else:
            print("Error creating user:", response.status_code, response.text)
            return False

    def get_users(self):
        """Fetch all users from the JsnDrop database."""
        response = requests.get(f"{self.base_url}/users", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching users:", response.status_code, response.text)
            return None

    def validate_login(self, username, password):
        """Validate user credentials using JsnDrop database"""
        users = self.get_users()
        if users is not None:
            for user in users:
                if user["username"] == username and user["password"] == password:
                    return True
        return False

    def create_table(self):
        """Create table in the JsnDrop database if it doesn't exist."""
        data = {
            "name": 'users',
            "schema": {
                "username": "string",
                "password": "string"
            }
        }
        response = requests.post(f"{self.base_url}/tables", headers=self.headers, json=data)
        if response.status_code == 201:
            print("Table created successfully.")
        elif response.status_code == 409:
            print("Table already exists.")
        else:
            print("Error creating table:", response.status_code, response.text)