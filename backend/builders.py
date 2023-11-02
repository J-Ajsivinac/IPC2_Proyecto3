from controller import Controller


class MainBackend:
    def __init__(self, read):
        self.build = Config()
        self.dict_conf = self.build.config
        self.messages = []
        self.read = read
        self.ctrl = Controller()
        self.load_initial_data()

    def reset_data(self):
        resp, self.dict_conf = self.build.reset()
        if not resp:
            if len(self.messages) == 0:
                return {"type_r": 0, "msg": "No hay datos para reiniciar"}
            self.messages.clear()
            self.read.restet_db()
        self.messages.clear()
        self.read.restet_db()
        return {"type_r": 1, "msg": "Se ha reiniciado la base de datos"}

    def load_initial_data(self):
        self.read.load_initial_data(self.dict_conf)
        self.read.load_initial_msgs(self.messages)

    def load_config(self, xml_data):
        return self.read.read_config(xml_data, self.dict_conf, self.build)

    def load_messages(self, xml_data):
        return self.read.load_msg(xml_data, self.dict_conf, self.messages)

    def return_hashtags(self, start, end):
        if len(self.messages) == 0:
            response = {
                "message": "No hay mensajes cargados en el sistema",
                "data": "",
                "type_r": 0,
                "data_graph": "",
            }
            return response
        return self.ctrl.filter_hashtag(start, end, self.messages)

    def return_users(self, start, end):
        if len(self.messages) == 0:
            response = {
                "message": "No hay mensajes cargados en el sistema",
                "data": "",
                "type_r": 0,
                "data_graph": "",
            }
            return response
        return self.ctrl.filter_users(start, end, self.messages)

    def return_sentiments(self, start, end):
        if len(self.messages) == 0:
            response = {
                "message": "No hay mensajes cargados en el sistema",
                "data": "",
                "type_r": 2,
                "data_graph": "",
            }
            return response
        return self.ctrl.filter_sentiments(start, end, self.messages)

    def return_graph_s(self, start, end):
        return self.ctrl.data_graph_sentiments(start, end, self.messages)

    def return_graph_hash(self, start, end):
        return self.ctrl.data_graph_hashtags(start, end, self.messages)

    def return_graph_u(self, start, end):
        return self.ctrl.data_graph_hashtags(start, end, self.messages)


class Message:
    def __init__(self, date, users, hash_, type_m):
        self.users = users
        self.hash = hash_
        self.type = type_m
        self.date = date


class Config:
    def __init__(self):
        self.config = {
            "sentimientos_positivos": set(),
            "sentimientos_negativos": set(),
            "rechazar_positivos": set(),
            "rechazar_negativos": set(),
        }

    def reset(self):
        if all(not value for value in self.config.values()):
            return False, self.config
        self.config.clear()
        self.config = {}
        self.config = {
            "sentimientos_positivos": set(),
            "sentimientos_negativos": set(),
            "rechazar_positivos": set(),
            "rechazar_negativos": set(),
        }
        return True, self.config

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
