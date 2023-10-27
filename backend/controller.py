import re
from datetime import datetime
from collections import Counter
import copy
from flask import jsonify


class Controller:
    def calc_sent(self, s_words, s_dict: dict):
        count_pos = 0
        count_neg = 0
        list_words = re.split(r"[^\w@#]+", s_words)
        for word in list_words:
            positive = s_dict["sentimientos_positivos"]
            negative = s_dict["sentimientos_negativos"]
            for pos, neg in zip(positive, negative):
                if word == pos:
                    count_pos += 1
                elif word == neg:
                    count_neg += 1
        type_m = None
        if count_neg > count_pos:
            type_m = "negativo"
        elif count_pos > count_neg:
            type_m = "positivo"
        else:
            type_m = "neutro"
        return type_m

    def formatter_response(self, response: dict):
        reformatted_response = {
            "message": response["message"],
            "data": [],
            "type_r": response["type_r"],
            "data_graph": response["data_graph"],
        }
        if "response" in response:
            for date, value in response["response"].items():
                reformatted_response["data"].append({"date": date, "results": value})
        else:
            reformatted_response["data"].append({"date": None, "results": None})
        return reformatted_response

    def filter_hashtag(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")
        dictionary = {}
        hashtags_dates = {}
        for value in list_data:
            date = value.date
            hashtags = value.hash

            if date in hashtags_dates:
                # Agregar los hashtags del mensaje a la lista existente
                hashtags_copy = list(hashtags_dates[date])
                hashtags_copy.extend(hashtags)
                hashtags_dates[date] = hashtags_copy
            else:
                # Si la fecha no está en el diccionario, crear una nueva lista de hashtags
                hashtags_dates[date] = hashtags

        list_u = copy.deepcopy(self.only_dates(list_data))

        for v in list_u:
            current_date = v.date
            count = None
            current_date = datetime.strptime(current_date, "%d/%m/%Y")
            if date_start <= current_date <= date_end:
                hash_dates = hashtags_dates[v.date]
                count = Counter(hash_dates)
            if count is not None:
                dictionary[v.date] = count
        response = {}
        if len(dictionary) == 0:
            response["type_r"] = 0
            response["message"] = "No se encontradon datos"
            response["data_graph"] = None
        else:
            response_graph = self.data_graph_hashtags(start, end, list_data)
            response["type_r"] = 1
            response["message"] = "Si se encontraron datos"
            response["response"] = dictionary
            response["data_graph"] = response_graph["graph_data"]
        response_return = self.formatter_response(response)
        return response_return

    def filter_users(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")
        dictionary = {}
        users_date = {}
        for value in list_data:
            date = value.date
            user = value.users

            if date in users_date:
                # Agregar los user del mensaje a la lista existente
                hashtags_copy = list(users_date[date])
                hashtags_copy.extend(user)
                users_date[date] = hashtags_copy
            else:
                # Si la fecha no está en el diccionario, crear una nueva lista de hashtags
                users_date[date] = user

        # list_u = copy.deepcopy(list_data)
        list_u = copy.deepcopy(self.only_dates(list_data))

        for v in list_u:
            current_date = v.date
            count = None
            current_date = datetime.strptime(current_date, "%d/%m/%Y")
            if date_start <= current_date <= date_end:
                user_dates = users_date[v.date]
                count = Counter(user_dates)
            if count is not None:
                dictionary[v.date] = count
        response = {}
        if len(dictionary) == 0:
            response["type_r"] = 0
            response["message"] = "No se encontradon datos"
            response["data_graph"] = None
        else:
            response_graph = self.data_graph_users(start, end, list_data)
            response["type_r"] = 1
            response["message"] = "Si se encontraron datos"
            response["response"] = dictionary
            response["data_graph"] = response_graph["graph_data"]
        response_return = self.formatter_response(response)
        return response_return

    def filter_sentiments(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")
        dictionary = {}
        users_date = {}
        for value in list_data:
            date = value.date
            types = value.type

            if date in users_date:
                # Agregar los types del mensaje a la lista existente
                hashtags_copy = list(users_date[date])
                hashtags_copy.append(types)
                users_date[date] = hashtags_copy
            else:
                # Si la fecha no está en el diccionario, crear una nueva lista de hashtags
                users_date[date] = types
        list_u = copy.deepcopy(self.only_dates(list_data))
        for v in list_u:
            current_date = v.date
            results = {}
            current_date = self.converter_date(current_date)
            count_posit = 0
            count_neg = 0
            count_n = 0
            if date_start <= current_date <= date_end:
                for v1 in list_data:
                    date_temp = self.converter_date(v1.date)
                    if current_date == date_temp:
                        if v1.type == "positivo":
                            count_posit += 1
                        elif v1.type == "negativo":
                            count_neg += 1
                        else:
                            count_n += 1
                results["positivo"] = count_posit
                results["negativo"] = count_neg
                results["neutro"] = count_n
                dictionary[v.date] = results
        response = {}
        # print(dictionary.values())
        if len(dictionary.values()) == 0:
            response["type_r"] = 0
            response["message"] = "No se encontradon datos"
            response["data_graph"] = None
        else:
            response_graph = self.data_graph_sentiments(start, end, list_data)
            response["type_r"] = 1
            response["message"] = "Si se encontraron datos"
            response["response"] = dictionary
            response["data_graph"] = response_graph["graph_data"]
        response_return = self.formatter_response(response)
        return response_return

    def data_graph_sentiments(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")
        lbl_positive = "positivo"
        lbl_negative = "negativo"

        dictionary = {}
        list_u = copy.deepcopy(self.only_dates(list_data))
        count_posit = 0
        count_neg = 0
        count_n = 0
        for value in list_u:
            results = {}
            b_date = value.date
            b_date = datetime.strptime(b_date, "%d/%m/%Y")
            for v in list_data:
                current_date = v.date
                current_date = datetime.strptime(current_date, "%d/%m/%Y")
                if date_start <= current_date <= date_end:
                    if b_date == current_date:
                        if v.type == lbl_positive:
                            count_posit += 1
                        elif v.type == lbl_negative:
                            count_neg += 1
                        else:
                            count_n += 1
            results["positivo"] = count_posit
            results["negativo"] = count_neg
            results["neutro"] = count_n
            response = {}
            response["graph_data"] = results
        return response

    def only_dates(self, list_data: list):
        lista_u = []
        dates_u = set()
        for msg in list_data:
            date = msg.date
            if date not in dates_u:
                dates_u.add(msg)
                lista_u.append(msg)
        return lista_u

    def only_hashtags(self, list_data: list):
        lista_u = []
        dates_u = set()
        for msg in list_data:
            hash_ = msg.hash
            for hash_i in hash_:
                if hash_i not in dates_u:
                    dates_u.add(hash_i)
                    lista_u.append(hash_i)
        return lista_u

    def only_users(self, list_data: list):
        lista_u = []
        dates_u = set()
        for msg in list_data:
            users = msg.users
            for user in users:
                if user not in dates_u:
                    dates_u.add(user)
                    lista_u.append(user)
        return lista_u

    def list_by_dates(self, list_data: list):
        hashtags_dates = {}
        for value in list_data:
            date = value.date
            hashtags = value.hash

            if date in hashtags_dates:
                # Agregar los hashtags del mensaje a la lista existente
                hashtags_copy = list(hashtags_dates[date])
                hashtags_copy.extend(hashtags)
                hashtags_dates[date] = hashtags_copy
            else:
                # Si la fecha no está en el diccionario, crear una nueva lista de hashtags
                hashtags_dates[date] = hashtags
        return hashtags_dates

    def list_by_dates_users(self, list_data: list):
        users_dates = {}
        for value in list_data:
            date = value.date
            users = value.users

            if date in users_dates:
                # Agregar los users del mensaje a la lista existente
                hashtags_copy = list(users_dates[date])
                hashtags_copy.extend(users)
                users_dates[date] = hashtags_copy
            else:
                # Si la fecha no está en el diccionario, crear una nueva lista de users
                users_dates[date] = users
        return users_dates

    def converter_date(self, string):
        date = datetime.strptime(string, "%d/%m/%Y")
        return date

    def data_graph_hashtags(self, start, end, list_data: list):
        date_start = self.converter_date(start)
        date_end = self.converter_date(end)

        hashtag_dates = self.list_by_dates(list_data)
        dictionary = {}
        list_u = copy.deepcopy(self.only_hashtags(list_data))
        for v in list_u:
            current_hashtag = v
            count = 0
            for date, values in hashtag_dates.items():
                current_date = self.converter_date(date)
                if date_start <= current_date <= date_end:
                    for value in values:
                        if value == current_hashtag:
                            count += 1
            if count > 0:
                dictionary[current_hashtag] = count
        response = {}
        response["graph_data"] = dictionary
        return response

    def data_graph_users(self, start, end, list_data: list):
        date_start = self.converter_date(start)
        date_end = self.converter_date(end)

        hashtag_dates = self.list_by_dates_users(list_data)
        dictionary = {}
        list_u = copy.deepcopy(self.only_users(list_data))
        for v in list_u:
            current_hashtag = v
            count = 0
            for date, values in hashtag_dates.items():
                current_date = self.converter_date(date)
                if date_start <= current_date <= date_end:
                    for value in values:
                        if value == current_hashtag:
                            count += 1
            if count > 0:
                dictionary[current_hashtag] = count
        response = {}
        response["graph_data"] = dictionary
        return response
