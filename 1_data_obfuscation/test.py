import unittest
from utils.xml_obfuscator import XMLObfuscator
import os
from pathlib import Path


class TestXMLObfuscator(unittest.TestCase):
    def setUp(self):
        self.sample_xml = "<data><person><name>Michael Jordan</name><age>60</age></person></data>"
        self.test_dir = './tests'

        if not Path(self.test_dir).exists():
            os.mkdir(self.test_dir)

        self.input_file = f"{self.test_dir}/input.xml"
        self.obfuscate_file = f"{self.test_dir}/obfuscate.xml"
        self.deobfuscate_file = f"{self.test_dir}/deobfuscate.xml"

        with open(self.input_file, "w") as f:
            f.write(self.sample_xml)
            f.close()

    def test_obfuscate(self):
        xml_obfuscator = XMLObfuscator(self.input_file)
        xml_obfuscator.obfuscate_text_elements()
        xml_obfuscator.save(self.obfuscate_file)

        with open(self.obfuscate_file, "r") as f:
            obfuscated_xml = f.read()

        self.assertNotEqual(obfuscated_xml, self.sample_xml)

    def test_deobfuscate(self):
        xml_obfuscator = XMLObfuscator(self.obfuscate_file)
        xml_obfuscator.deobfuscate_text_elements()
        xml_obfuscator.save(self.deobfuscate_file)

        with open(self.deobfuscate_file, "r") as f:
            deobfuscated_xml = f.read()

        self.assertEqual(deobfuscated_xml, self.sample_xml)


if __name__ == '__main__':
    unittest.main()
