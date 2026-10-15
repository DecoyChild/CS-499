# Class to create a user when one is logged into the app
class User:
    def __init__(self):
        self.username = None

    def __init__(self,name:str):
        self.username = name

    def set_username(self, name:str):
        self.username = name