import re
from datetime import datetime
from collections import Counter
import copy


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
        return count_pos, count_neg, type_m

    def filter_hashtag(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")
        dictionary = {}
        # list_u = set(list_data)
        hashtags_dates = {}
        # hashtags_dates.clear()
        # hashtags_dates.popitem()
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

        # list_u = copy.deepcopy(list_data)
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

        return dictionary

    def filter_users(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")
        dictionary = {}
        # list_u = set(list_data)
        users_date = {}
        # users_date.clear()
        # users_date.popitem()
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

        return dictionary

    def filter_sentiments(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")
        lbl_positive = "positivo"
        lbl_negative = "negativo"

        dictionary = {}
        list_u = copy.deepcopy(self.only_dates(list_data))
        for value in list_u:
            results = {}
            count_posit = 0
            count_neg = 0
            count_n = 0
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
            dictionary[value.date] = results
        return dictionary

    def only_dates(self, list_data: list):
        lista_u = []
        dates_u = set()
        for msg in list_data:
            date = msg.date
            if date not in dates_u:
                dates_u.add(msg)
                lista_u.append(msg)
        return lista_u
