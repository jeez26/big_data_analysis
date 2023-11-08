from OpenSSL import crypto


class CertificateGenerator:
    def __init__(self, common_name, private_key_file, certificate_file, p12_file, password):
        self.common_name = common_name
        self.private_key_file = private_key_file
        self.certificate_file = certificate_file
        self.p12_file = p12_file
        self.password = password

        self._key = None
        self._cert = None

    def generate_key(self):
        # Создаем ключ (key)
        self._key = crypto.PKey()
        self._key.generate_key(crypto.TYPE_RSA, 2048)

    def generate_certificate(self):
        if not self._key:
            raise Exception("Key is not generated!")

        # Создаем цифровой сертификат X.509
        cert = crypto.X509()
        cert.get_subject().CN = self.common_name
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(self._key)
        cert.sign(self._key, 'sha256')

        self._cert = cert

        # Сохраняем сертификат в файл
        with open(self.certificate_file, "wb") as certfile:
            certfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        print("The certificate were created successfully.")

    def generate_p12(self):
        if not self._key:
            raise Exception("Key is not generated!")

        # Создаем хранилище ключей PKCS12
        p12 = crypto.PKCS12()
        p12.set_privatekey(self._key)
        p12.set_certificate(self._cert)
        with open(self.p12_file, "wb") as p12file:
            p12file.write(p12.export(passphrase=self.password))

        print("The PKCS12 keystore were created successfully.")
