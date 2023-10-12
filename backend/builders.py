class Message:
    def __init__(self, date, users, hash_, type_m):
        self.users = users
        self.hash = hash_
        self.type = type_m
        self.date = date


class Config:
    def __init__(self):
        self.positive = []
        self.negative = []
