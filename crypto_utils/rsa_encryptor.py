from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import os

class RSAEncryptor():
    def __init__(self,priv_path="/config/private.pem",pub_path="public.pem"):
        self.priv_path=priv_path
        self.pub_path=pub_path
        if os.path.exists(self.priv_path):
            with open(self.priv_path,"rb") as priv:
                self.private_key = RSA.importKey(priv.read())
            self.public_key = self.private_key.publickey()
        else:
            self.private_key = RSA.generate(2048)
            self.public_key = self.private_key.publickey()
            self.save_keys_to_file()
    def save_keys_to_file(self):
        with open(self.priv_path, 'wb') as content_file:
            os.chmod(self.priv_path, 0o600)  # use an 0o prefix for octal integers
            content_file.write(self.private_key.exportKey('PEM'))
        with open(self.pub_path, 'wb') as content_file:
            content_file.write(self.public_key.exportKey('OpenSSH'))

    def get_private_key(self):
        return self.private_key
    def get_public_key(self):
        return self.public_key
    def encrypt(self,data :str , recipient_public_key_bytes: bytes) ->str :
        #encryption
        recipient_public_key = RSA.import_key(recipient_public_key_bytes)
        cipher = PKCS1_OAEP.new(recipient_public_key)
        encrypted_data = cipher.encrypt(data.encode('utf-8'))
        return base64.b64encode(encrypted_data).decode('utf-8')

    def decrypt(self, encrypted_message_b64: str) -> str:
        #decryption
        encrypted = base64.b64decode(encrypted_message_b64)
        cipher = PKCS1_OAEP.new(self.private_key)
        decrypted = cipher.decrypt(encrypted)
        return decrypted.decode('utf-8')