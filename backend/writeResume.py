import xml.etree.ElementTree as ET
from xml.dom import minidom
from builders import Message


class Write:
    def group_dates(self, list_data: list):
        users_date = {}

        for value in list_data:
            date = value.date
            users = value.users
            hashtags = value.hash

            if date not in users_date:
                users_date[date] = Message(date, set(), set(), 0)

            new_users = [user for user in users if user not in users_date[date].users]
            new_hashtags = [
                hashtag for hashtag in hashtags if hashtag not in users_date[date].hash
            ]
            # print(new_hashtags)
            users_date[date].users.update(new_users)
            users_date[date].hash.update(new_hashtags)
            users_date[date].type += 1

        return users_date

    def write_resume(self, list_data: list):
        date_users = self.group_dates(list_data)
        # print(date_users)
        root = ET.Element("MENSAJES_RECIBIDOS")

        for _, value in date_users.items():
            # print(value.users)
            tiempo = ET.SubElement(root, "TIEMPO")
            date = ET.SubElement(tiempo, "FECHA")
            date.text = f"{value.date}"
            msj_r = ET.SubElement(tiempo, "MSJ_RECIBIDOS")
            msj_r.text = f"{value.type}"
            usr_m = ET.SubElement(tiempo, "USR_MENCIONADOS")
            usr_m.text = f"{len(value.users)}"
            hash_in = ET.SubElement(tiempo, "HASH_INCLUIDOS")
            hash_in.text = f"{len(value.hash)}"

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        return xmlstr
        # with open(ruta, "w", encoding="utf-8") as f:
        #     f.write(xmlstr)

    def write_resume_confif(self, ruta, list_data: dict):
        root = ET.Element("CONFIG_RECIBIDA")
        positive = ET.SubElement(root, "PALABRAS_POSITIVAS")
        positive.text = f'{len(list_data["sentimientos_positivos"])}'

        recha_p = ET.SubElement(root, "PALABRAS_POSITIVAS_RECHAZADA")
        recha_p.text = f'{len(list_data["rechazar_positivos"])}'

        negative = ET.SubElement(root, "PALABRAS_NEGATIVAS")
        negative.text = f'{len(list_data["sentimientos_negativos"])}'

        recha_n = ET.SubElement(root, "PALABRAS_NEGATIVAS_RECHAZADA")
        recha_n.text = f'{len(list_data["rechazar_negativos"])}'

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        return xmlstr
        # with open(ruta, "w", encoding="utf-8") as f:
        #     f.write(xmlstr)
