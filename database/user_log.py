import os

class Users:
    _instance = None
    USER_LIST = "".join([os.getcwd(), "/database/users.txt"])

    def qtd(self):
        with open(Users.USER_LIST, 'r') as fp:
            return len(fp.readlines())
    
    def write(self, new_id):
        with open(Users.USER_LIST, 'a') as fp:
            fp.write(f"{new_id}\n")
    
    def read(self):
        with open(Users.USER_LIST, 'r') as fp:
            return fp.read()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance




