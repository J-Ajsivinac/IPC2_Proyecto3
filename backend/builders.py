class Message:
    def __init__(self, date, users, hash_, type_m):
        self.users = users
        self.hash = hash_
        self.type = type_m
        self.date = date


class Config:
    def __init__(self):
        self.config = {
            "sentimientos_positivos": [],
            "sentimientos_negativos": [],
            "rechazar_positivos": [],
            "rechazar_negativos": [],
        }

    def verify_sent(self, current_sent, value):
        search_in = (
            "sentimientos_negativos"
            if current_sent == "sentimientos_positivos"
            else "sentimientos_positivos"
        )

        if search_in in self.config:
            if value in self.config[search_in]:
                response = (
                    "rechazar_negativos"
                    if search_in == "sentimientos_positivos"
                    else "rechazar_positivos"
                )
                return response
            else:
                return current_sent

        return "Error"
