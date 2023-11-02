import xml.etree.ElementTree as ET
from xml.dom import minidom
from builders import Config
from unidecode import unidecode
from controller import Controller
from builders import Message
from writeResume import Write
import os
import re


class Read:
    def read_config(self, content, conf: dict, Config):
        current = {
            "sentimientos_positivos": set(),
            "sentimientos_negativos": set(),
            "rechazar_positivos": set(),
            "rechazar_negativos": set(),
        }
        db_root_file = self.write_file_config()
        db_tree = ET.parse(db_root_file)
        db_root = db_tree.getroot()
        root = ET.fromstring(content)
        first = None
        second = None
        for child in root:
            first = child.tag
            second = (
                "sentimientos_negativos"
                if first == "sentimientos_positivos"
                else "sentimientos_positivos"
            )
            break
        # print(first, second)
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
                current[response].add(text)
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
                    # db_second.append(new_element)
                    if not self.verify_dup(text, conf[response]):
                        db_second.append(new_element)
                    conf[response].add(text)
                    current[response].add(text)

        write = Write()
        xmlstr1 = write.write_resume_confif(root, current)

        xmlstr = minidom.parseString(ET.tostring(db_root)).toprettyxml(indent="    ")

        # Eliminar los saltos de linea adicionales
        xmlstr = "\n".join([line for line in xmlstr.split("\n") if line.strip()])
        with open(db_root_file, "w", encoding="utf-8") as f:
            f.write(xmlstr)

        return xmlstr1

    def write_file_config(self):
        _root_file = os.path.dirname(os.path.abspath(__file__))
        db_config = os.path.join(_root_file, "DB", "config.xml").replace("\\", "\\\\")
        try:
            tree = ET.parse(db_config)
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
            with open(db_config, "w+", encoding="utf-8") as f:
                f.write(xmlstr)
        return db_config

    def write_file_messages(self):
        _root_file = os.path.dirname(os.path.abspath(__file__))
        db_msg = os.path.join(_root_file, "DB", "messages.xml").replace("\\", "\\\\")
        try:
            tree = ET.parse(db_msg)
            root = tree.getroot()
        except ET.ParseError:
            root = ET.Element("datos")
            tree = ET.ElementTree(
                root
            )  # ET.SubElement(element_s,"palabra").text = "XD"
            xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
            with open(db_msg, "w+", encoding="utf-8") as f:
                f.write(xmlstr)
        return db_msg

    def load_initial_data(self, conf: dict):
        db_root_file = self.write_file_config()
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

    def load_initial_msgs(self, list_msg: list):
        db_root_file = self.write_file_messages()
        db_tree = ET.parse(db_root_file)
        db_root = db_tree.getroot()

        for data in db_root.findall("mensaje"):
            tipo = data.findtext("tipo")
            fecha = data.findtext("fecha")
            users = []
            for user in data.find("usuarios"):
                users.append(user.text)
            hastags = []
            for hashtag in data.find("hashtags"):
                hastags.append(hashtag.text)
            list_msg.append(Message(fecha, users, hastags, tipo))

    def to_unicode(self, data):
        string = data.lower()
        string = string.strip()
        string = unidecode(string)
        return string

    def load_msg(self, content, conf: dict, list_msg: list):
        temp = []
        db_root_file = self.write_file_messages()
        db_tree = ET.parse(db_root_file)
        db_root = db_tree.getroot()

        root = ET.fromstring(content)
        patter_date = r"\d{2}/\d{2}/\d{4}"
        patter_users = r"@([A-Za-z0-9_]+)"
        pattern_hastag = r"#([A-Za-z0-9_]+)#"
        # mensaje = None
        # mensajes = db_root.find("datos")
        read = Write()

        for msg in root.findall("MENSAJE"):
            search_date = []
            search_users = set()
            search_hastag = set()
            date_read = msg.findtext("FECHA")
            msg_read = msg.findtext("TEXTO")
            msg_read = self.to_unicode(msg_read)

            mensaje = ET.SubElement(db_root, "mensaje")
            if re.search(patter_date, date_read) is None:
                continue
            search_date.append(re.search(patter_date, date_read).group(0))
            search_users.update(re.findall(patter_users, msg_read))
            search_users = ["@" + user for user in search_users]

            search_hastag.update(re.findall(pattern_hastag, msg_read))
            search_hastag = ["#" + hashtag + "#" for hashtag in search_hastag]
            msg_read = msg_read.lower()
            type_m = Controller.calc_sent(Controller, msg_read, conf)

            tipo = ET.SubElement(mensaje, "tipo")
            tipo.text = f"{type_m}"
            fecha = ET.SubElement(mensaje, "fecha")
            fecha.text = f"{search_date[0]}"
            usuarios = ET.SubElement(mensaje, "usuarios")
            for user in search_users:
                usuario = ET.SubElement(usuarios, "usuario")
                usuario.text = f"{user}"
            hashtags = ET.SubElement(mensaje, "hashtags")
            for h in search_hastag:
                hashtag = ET.SubElement(hashtags, "hashtag")
                hashtag.text = f"{h}"
            # tipo.text = f"{type_m}"

            message = Message(search_date[0], set(), set(), type_m)
            message.users.update(search_users)
            message.hash.update(search_hastag)

            list_msg.append(message)
            temp.append(message)

            if mensaje is None:
                continue

            xmlstr = minidom.parseString(ET.tostring(db_root)).toprettyxml(
                indent="    "
            )
            xmlstr = "\n".join([line for line in xmlstr.split("\n") if line.strip()])

            with open(db_root_file, "w+", encoding="utf-8") as f:
                f.write(xmlstr)
        # print(search_date, search_users, search_hastag)
        xml1 = read.write_resume(temp)
        return xml1

    def verify_dup(self, value, list_w: list):
        if value in list_w:
            return True

        return False

    def restet_db(self):
        _root_file = os.path.dirname(os.path.abspath(__file__))
        # add_data = ET.fromstring(data)
        db_config = os.path.join(_root_file, "DB", "config.xml").replace("\\", "\\\\")
        db_messages = os.path.join(_root_file, "DB", "messages.xml").replace(
            "\\", "\\\\"
        )
        with open(db_config, "w", encoding="utf-8") as file:
            file.write("")
        with open(db_messages, "w", encoding="utf-8") as file:
            file.write("")
