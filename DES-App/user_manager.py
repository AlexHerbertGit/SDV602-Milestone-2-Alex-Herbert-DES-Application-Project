from jsn_drop_service import jsnDrop
from datetime import datetime

class UserManager(object):
    
    current_user = None  # Username of logged in user
    current_pass = None  # Password of logged in user
    current_status = None  # Login status (Logged In/Out)
    current_screen = None  # Which screen they're looking at
    jsn_tok = "39d0f8d6-bb55-4158-b364-72a33642e8ef"

    def __init__(self):
        
        super().__init__()
        # Connect to JSNDrop service
        self.jsnDrop = jsnDrop(UserManager.jsn_tok, "https://newsimland.com/~todd/JSON")
        result = self.jsnDrop.create(
            "tblUser",
            {
                "PersonID PK": "A_LOOONG_NAME" + ("X" * 50),
                "Password": "A_LOOONG_PASSWORD" + ("X" * 50),
                "Status": "STATUS_STRING",  # Logged In/Out/Registered
            },
        )

        # Create chat table
        self.init_chat()

    def register(self, user_id, password):
        """
        Register User function
        
        """
        api_result = self.jsnDrop.select("tblUser", f"PersonID = '{user_id}'")
        if "DATA_ERROR" in self.jsnDrop.jsnStatus:  # Username not found
            result = self.jsnDrop.store(
                "tblUser",
                [{"PersonID": user_id, "Password": password, "Status": "Registered"}],
            )
            return "Registration Success"
        else:
            return "User Already Exists"

    def login(self, user_id, password):
        """
        Login function
        """
        api_result = self.jsnDrop.select(
            "tblUser", f"PersonID = '{user_id}' AND Password = '{password}'"
        )
        if "DATA_ERROR" in self.jsnDrop.jsnStatus:
            UserManager.current_status = "Logged Out"
            UserManager.current_user = None
            return "Login Failed"
        else:
            UserManager.current_status = "Logged In"
            UserManager.current_user = user_id
            UserManager.current_pass = password
            self.jsnDrop.store(
                "tblUser",
                [{"PersonID": user_id, "Password": password, "Status": "Logged In"}],
            )
            return "Login Success"

    def logout(self):
        """
        Logout function
        """
        if UserManager.current_status == "Logged In":
            api_result = self.jsnDrop.store(
                "tblUser",
                [{
                    "PersonID": UserManager.current_user,
                    "Password": UserManager.current_pass,
                    "Status": "Logged Out",
                }],
            )
            if not "ERROR" in api_result:
                UserManager.current_status = "Logged Out"
                return "Logged Out"
            return self.jsnDrop.jsnStatus
        return "Must be 'Logged In' to 'LogOut'"

    def get_current_user(self):
        """Gets username of logged in user"""
        return UserManager.current_user

    def is_logged_in(self):
        """Checks if someone is logged in"""
        return UserManager.current_status == "Logged In"

    def set_current_DES(self, DESScreenIndex):
        """
        This saves the current DES screen
        
        """
        result = None
        if UserManager.current_status == "Logged In":
            UserManager.current_screen = DESScreenIndex
            result = "Set Screen"
        else:
            result = "Log in to allocate the current DES screen"
        return result

    def get_current_screen(self):
        """Gets which screen user is looking at"""
        return UserManager.current_screen

    def init_chat(self):
        """
        Chat initiation function
        """
        result = self.jsnDrop.create(
            "tblChatV2",
            {
                "PersonID": "A_LOOONG_NAME" + ("X" * 50),
                "DESNumber": "A_LOOONG_DES_ID" + ("X" * 50),
                "Chat": "A_LOONG____CHAT_ENTRY" + ("X" * 255),
                "Time": datetime.now().timestamp(),
            },
        )
        return result

    def chat(self, message):
        """
        Saves a new chat message
        """
        result = None
        if UserManager.current_status != "Logged In":
            result = "You must be logged in to use the chat feature"
        elif UserManager.current_screen == None:
            result = "Message not sent. Current DES window must be set."
        else:
            user_id = UserManager.current_user
            des_screen = UserManager.current_screen
            current_time = datetime.now().timestamp()
            api_result = self.jsnDrop.store(
                "tblChatV2",
                [{
                    "PersonID": user_id,
                    "DESNumber": f"{des_screen}",
                    "Chat": message,
                    "Time": current_time,
                }],
            )
            print(f"Storing chat message: {message}")  
            if "ERROR" in api_result:
                result = self.jsnDrop.jsnStatus
            else:
                result = "Chat sent"
        return result

    def get_chat(self):
        """
        Fetches Chat messages and checks the user is logged.
        """
        result = None
        if UserManager.current_status == "Logged In":
            des_screen = UserManager.current_screen
            if not (des_screen is None):
                api_result = self.jsnDrop.select(
                    "tblChatV2", f"DESNumber = '{des_screen}'"
                )
                if not ("DATA_ERROR" in api_result):
                    result = self.jsnDrop.jsnResult
                    # Sort messages by time
                    if result:
                        print(f"Got chat messages: {len(result)}")  # Help me debug
                        try:
                            result = sorted(result, key=lambda x: float(x["Time"]))
                        except Exception as e:
                            print(f"Error sorting messages: {str(e)}")
        return result