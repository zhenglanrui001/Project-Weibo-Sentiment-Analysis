class User:
    id = None
    username = None
    password = None
    createtime = None

    def __init__(self, username, password):
        self.username = username
        self.password = password
