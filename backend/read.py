import xml.etree.ElementTree as ET
from xml.dom import minidom
from builders import Config
from unidecode import unidecode
from controller import Controller
from builders import Message
import os
import re


class Read:
    def read_config(self, content, conf: dict, Config):
        db_root_file = self.write_file()
        db_tree = ET.parse(db_root_file)
        db_root = db_tree.getroot()
        root = ET.fromstring(content)
        first = None
        second = None
        for name in ["sentimientos_positivos", "sentimientos_negativos"]:
            element = root.find(name)
            if element is not None:
                first = name
                second = (
                    "sentimientos_negativos"
                    if name == "sentimientos_positivos"
                    else "sentimientos_positivos"
                )
                break
        if first is not None:
            db_first = db_root.find(first)
            for element in root.find(first):
                text = element.text.lower()
                text = text.strip()
                text = unidecode(text)
                response = Config.verify_sent(first, text)
                if response != first:
                    db_first = db_root.find(response)
                new_element = ET.Element("palabra")
                new_element.text = text
                if not self.verify_dup(text, conf[response]):
                    db_first.append(new_element)
                conf[response].add(text)
        if second is not None:
            db_second = root.find(second)
            if db_second is not None:
                db_second = db_root.find(second)
                for element in root.find(second):
                    text = element.text.lower()
                    text = text.strip()
                    text = unidecode(text)
                    response = Config.verify_sent(second, text)
                    if response != second:
                        db_second = db_root.find(response)
                    new_element = ET.Element("palabra")
                    new_element.text = text
                    db_second.append(new_element)
                    if not self.verify_dup(text, conf[response]):
                        db_first.append(new_element)
                    conf[response].add(text)

        xmlstr = minidom.parseString(ET.tostring(db_root)).toprettyxml(indent="    ")

        # Eliminar los saltos de linea adicionales
        xmlstr = "\n".join([line for line in xmlstr.split("\n") if line.strip()])
        with open(db_root_file, "w", encoding="utf-8") as f:
            f.write(xmlstr)

    def write_file(self):
        _root_file = os.path.dirname(os.path.abspath(__file__))
        # add_data = ET.fromstring(data)
        db = os.path.join(_root_file, "DB", "config.xml").replace("\\", "\\\\")
        try:
            tree = ET.parse(db)
            root = tree.getroot()
        except ET.ParseError:
            root = ET.Element("diccionario")
            tree = ET.ElementTree(root)

            element_s = root.find("sentimientos_positivos")
            if element_s is None:
                element_s = ET.SubElement(root, "sentimientos_positivos")

            element_s = root.find("sentimientos_negativos")
            if element_s is None:
                element_s = ET.SubElement(root, "sentimientos_negativos")

            element_s = root.find("rechazar_positivos")
            if element_s is None:
                element_s = ET.SubElement(root, "rechazar_positivos")

            element_s = root.find("rechazar_negativos")
            if element_s is None:
                element_s = ET.SubElement(root, "rechazar_negativos")

            # ET.SubElement(element_s,"palabra").text = "XD"
            xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
            with open(db, "w+", encoding="utf-8") as f:
                f.write(xmlstr)
        return db

    def load_initial_data(self, conf: dict):
        db_root_file = self.write_file()
        db_tree = ET.parse(db_root_file)
        db_root = db_tree.getroot()

        for data in db_root.find("sentimientos_positivos"):
            conf["sentimientos_positivos"].add(data.text)

        for data in db_root.find("sentimientos_negativos"):
            conf["sentimientos_negativos"].add(data.text)

        for data in db_root.find("rechazar_positivos"):
            conf["rechazar_positivos"].add(data.text)

        for data in db_root.find("rechazar_negativos"):
            conf["rechazar_negativos"].add(data.text)

    def load_msg(self, content, conf: dict, list_msg: list):
        root = ET.fromstring(content)
        patter_date = r"\d{2}/\d{2}/\d{4}"
        patter_users = r"@([A-Za-z0-9_]+)"
        pattern_hastag = r"#([A-Za-z0-9_]+)#"

        for msg in root.findall("MENSAJE"):
            search_date = []
            search_users = []
            search_hastag = []
            date_read = msg.findtext("FECHA")
            msg_read = msg.findtext("TEXTO")

            search_date.append(re.search(patter_date, date_read).group(0))
            search_users.extend(re.findall(patter_users, msg_read))
            search_hastag.extend(re.findall(pattern_hastag, msg_read))
            _, _, type_m = Controller.calc_sent(Controller, msg_read, conf)
            list_msg.append(Message(search_date, search_users, search_hastag, type_m))

        # print(search_date, search_users, search_hastag)

    def verify_dup(self, value, list_w: list):
        if value in list_w:
            return True

        return False
