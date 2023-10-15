import re
from datetime import datetime


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
        for value in list_data:
            results = []
            current_date = value.date
            current_date = datetime.strptime(current_date, "%d/%m/%Y")
            if date_start <= current_date <= date_end:
                results.extend(value.hash)
            dictionary[value.date] = results
        return dictionary

    def filter_users(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")

        dictionary = {}
        for value in list_data:
            results = []
            current_date = value.date
            current_date = datetime.strptime(current_date, "%d/%m/%Y")
            if date_start <= current_date <= date_end:
                results.extend(value.users)
            dictionary[value.date] = results
        return dictionary

    def filter_sentiments(self, start, end, list_data: list):
        date_start = datetime.strptime(start, "%d/%m/%Y")
        date_end = datetime.strptime(end, "%d/%m/%Y")
        lbl_positive = "positivo"
        lbl_negative = "negativo"

        dictionary = {}
        list_u = set(list_data)
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
