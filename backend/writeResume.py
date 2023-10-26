import xml.etree.ElementTree as ET
from xml.dom import minidom
from builders import Message


class Write:
    def group_dates(self, list_data: list):
        users_date = {}
        for value in list_data:
            date = value.date
            if date in users_date:
                users_date[date].users += len(value.users)
                users_date[date].hash += len(value.hash)
                users_date[date].type += 1
            else:
                users_date[date] = Message(
                    value.date, len(value.users), len(value.hash), 1
                )
        return users_date

    def write_resume(self, ruta, list_data: list):
        date_users = self.group_dates(list_data)
        # print(date_users)
        root = ET.Element("MENSAJES_RECIBIDOS")

        for _, value in date_users.items():
            # print(value.users)
            tiempo = ET.SubElement(root, "TIEMPO")
            msj_r = ET.SubElement(tiempo, "MSJ_RECIBIDO")
            msj_r.text = f"{value.type}"
            usr_m = ET.SubElement(tiempo, "USR_MENCIONADOS")
            usr_m.text = f"{value.users}"
            hash_in = ET.SubElement(tiempo, "HASH_INCLUIDOS")
            hash_in.text = f"{value.hash}"

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(xmlstr)

    def write_resume_confif(self, ruta, list_data: dict):
        root = ET.Element("CONFIG_RECIBIDA")
        positive = ET.SubElement(root, "PALABRAS_POSITIVAS")
        positive.text = f'{len(list_data["sentimientos_positivos"])}'
        recha_p = ET.SubElement(root, "PALABRAS_POSITIVAS_RECHAZADA")
        recha_p.text = f'{len(list_data["rechazar_positivos"])}'
        negative = ET.SubElement(root, "PALABRAS_NEGATIVAS")
        negative.text = f'{len(list_data["sentimientos_negativos"])}'
        recha_n = ET.SubElement(root, "RECHAZAR_NEGATIVOS")
        recha_n.text = f'{len(list_data["rechazar_negativos"])}'

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(xmlstr)
