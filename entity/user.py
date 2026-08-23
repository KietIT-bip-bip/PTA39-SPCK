class User:
    def __init__(self, username, email, password):
        self.__username = username
        self.__email = email
        self.__password = password
    
    def __str__(self):
        return f"User(username={self.__username}, email={self.__email})"
    
    # Getter methods
    def get_username(self):
        return self.__username
    
    def get_email(self):
        return self.__email
    
    def get_password(self):
        return self.__password
    
    # Setter methods
    def set_username(self, username:str):
        if username and len(username) > 6: self.__username = username
        else: print("Username must be at least 6 characters long.")
        
    def set_email(self, email:str):
        if email and "@" in email: self.__email = email
        else: print("Invalid email address.")
        
    def set_password(self, password:str):
        if password and len(password) > 8: self.__password = password
        else: print("Password must be at least 8 characters long.")
        
    # -----------------------------
    def to_dict(self):
        return {
            "username": self.__username,
            "email": self.__email,
            "password": self.__password
        }
        
    # chuyen tu dict sang object
    @classmethod
    def from_dict(cls, data): 
        return cls(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password")
        )
    