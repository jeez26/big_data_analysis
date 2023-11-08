import sys
from utils.xml_obfuscator import XMLObfuscator
from pathlib import Path


def main():
    if len(sys.argv) != 4:
        raise ValueError("Usage: python xml_obfuscator.py <mode> <input_file> <output_file>")

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if not Path(input_file).exists():
        raise FileExistsError(f"File '{input_file}' don't exist!")

    if mode != "obfuscate" and mode != "deobfuscate":
        raise ValueError("Invalid mode. Use 'obfuscate' or 'deobfuscate'.")

    xml_obfuscator = XMLObfuscator(input_file)

    if mode == "obfuscate":
        xml_obfuscator.obfuscate_text_elements()
        xml_obfuscator.save(output_file)
        print(f"The XML file has been successfully obfuscated. Please check: '{output_file}'")
    else:
        xml_obfuscator.deobfuscate_text_elements()
        xml_obfuscator.save(output_file)
        print(f"The XML file has been successfully deobfuscated. Please check: '{output_file}'")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")
