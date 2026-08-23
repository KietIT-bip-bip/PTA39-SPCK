from JSON.data_io import DataIO
from entity import User


class UserList:
    def __init__(self):
        self.__users = []
        
    def add_user(self, user: User):
        if isinstance(user, User):
            # kiem tra trung lap username + email
            if any(u.get_username() == user.get_username() or u.get_email() == user.get_email() for u in self.__users):
                print("A user with the same username or email already exists.")
                return
            self.__users.append(user)
        else:
            print("Only User instances can be added.")
        
    def remove_user(self, username: str):
        for user in self.__users:
            if user.get_username() == username:
                self.__users.remove(user)
                return
        print(f"User with username '{username}' not found.")
        
    def get_user(self, username: str):
        for user in self.__users:
            if user.get_username() == username:
                return user
        print(f"User with username '{username}' not found.")
        return None
    
    def update_user(self, user:User):
        # xoa cu + them moi
        self.remove_user(user.get_username())
        self.add_user(user)
        
    def print_user_list(self):
        for user in self.__users:
            print(user)
            print("------------------")
                
    def get_users(self):
        return self.__users
    
    # dict -> object
    def load_from_json(self, file_path: str):
        try:
            data_list = DataIO.read_json(file_path)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return
        except Exception as e:
            print(f"Error while reading '{file_path}': {e}")
            return

        self.__users = []
        for data in data_list:
            try:
                user = User.from_dict(data)
                self.__users.append(user)
            except Exception as e:
                print(f"Error while parsing user data {data}: {e}")
    
    # object -> dict (save json)
    def save_to_json(self, file_path: str):
        """Chuyen list User thanh list dict roi luu ra file json."""
        data_list = [user.to_dict() for user in self.__users]
        DataIO.write_json(file_path, data_list)