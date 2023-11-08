import unittest
import os
from tempfile import TemporaryDirectory
from utils.pkcs12 import CertificateGenerator
from utils.utils import decrypt_message, crypt_message


class TestCertificateGenerator(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.common_name = "Test Certificate"
        self.private_key_file = "private_key.pem"
        self.certificate_file = "certificate.pem"
        self.p12_file = "certificate.p12"
        self.password = b"testpassword"
        self.message = b'This is a secret message.'

    def test_generate_certificate_and_p12(self):
        with TemporaryDirectory() as temp_dir:
            private_key_file = os.path.join(temp_dir, self.private_key_file)
            certificate_file = os.path.join(temp_dir, self.certificate_file)
            p12_file = os.path.join(temp_dir, self.p12_file)

            generator = CertificateGenerator(
                self.common_name, private_key_file, certificate_file, p12_file, self.password
            )
            generator.generate_key()
            generator.generate_certificate()
            generator.generate_p12()

            # Assert that files are created
            self.assertTrue(os.path.exists(certificate_file))
            self.assertTrue(os.path.exists(p12_file))

    def test_success_decrypt(self):
        certificate_generator = CertificateGenerator(self.common_name,
                                                     self.private_key_file,
                                                     self.certificate_file,
                                                     self.p12_file,
                                                     self.password)
        certificate_generator.generate_key()
        certificate_generator.generate_certificate()
        certificate_generator.generate_p12()

        with open(self.certificate_file, 'rb') as cert_file:
            cert_data = cert_file.read()

        with open(self.p12_file, 'rb') as p12_file:
            p12_data = p12_file.read()

        ciphertext = crypt_message(self.message, cert_data)
        plaintext = decrypt_message(self.password, p12_data, ciphertext)

        self.assertTrue(self.message.decode() == plaintext.decode())

    def test_wrong_password(self):
        certificate_generator = CertificateGenerator(self.common_name,
                                                     self.private_key_file,
                                                     self.certificate_file,
                                                     self.p12_file,
                                                     self.password)
        certificate_generator.generate_key()
        certificate_generator.generate_certificate()
        certificate_generator.generate_p12()

        with open(self.certificate_file, 'rb') as cert_file:
            cert_data = cert_file.read()

        with open(self.p12_file, 'rb') as p12_file:
            p12_data = p12_file.read()

        ciphertext = crypt_message(self.message, cert_data)
        try:
            plaintext = decrypt_message(b'wrongPass', p12_data, ciphertext)
        except ValueError:
            self.assertFalse(False)
            return

        self.assertTrue(self.message.decode() == plaintext.decode())


if __name__ == "__main__":
    unittest.main()
