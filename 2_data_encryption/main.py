from utils.pkcs12 import CertificateGenerator
from utils.utils import decrypt_message, crypt_message

if __name__ == '__main__':
    password = b"password12344321"
    message = b'This is a secret message.'

    certificate_generator = CertificateGenerator("Name",
                                                 "./data/private_key.pem",
                                                 "./data/public.cer",
                                                 "./data/private.p12",
                                                 password)
    certificate_generator.generate_key()
    certificate_generator.generate_certificate()
    certificate_generator.generate_p12()

    with open('./data/public.cer', 'rb') as cert_file:
        cert_data = cert_file.read()

    with open('./data/private.p12', 'rb') as p12_file:
        p12_data = p12_file.read()

    ciphertext = crypt_message(message, cert_data)
    plaintext = decrypt_message(password, p12_data, ciphertext)

    print(f"Original Message: {message.decode()}")
    print(f"Crypted Message: {ciphertext}")
    print(f"Decrypted Message: {plaintext.decode()}")
