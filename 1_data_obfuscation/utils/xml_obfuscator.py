import xml.etree.ElementTree as ElementTree
import base64


class XMLObfuscator:
    def __init__(self, xml_file):
        if not xml_file:
            raise ValueError("Incorrectly specified XML file!")

        self.tree = ElementTree.parse(xml_file)
        self.root = self.tree.getroot()

    def __process_text_elements(self, func):
        for elem in self.root.iter():
            if elem.text.strip():
                elem.text = func(elem.text)

    def obfuscate_text_elements(self):
        self.__process_text_elements(lambda text: base64.b64encode(text.encode()).decode())

    def deobfuscate_text_elements(self):
        self.__process_text_elements(lambda text: base64.b64decode(text).decode())

    def save(self, output_file):
        self.tree.write(output_file)
