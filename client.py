import socket
import threading
import os
from crypto_utils.rsa_encryptor import RSAEncryptor

nickname=input("Enter your nickname: ")
encryptor=RSAEncryptor()
public_key=encryptor.get_public_key()

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",55555))

public_keys={}
def receive():
    while True :
        try :
            data=client.recv(4069).decode('utf-8')
            if data =="nick":
                client.send(nickname.encode('utf-8'))
            elif data =="send_key":
                client.send(public_key.export_key())
            elif data.startswith("PUBKEY:"):
                # format: PUBKEY:nick:base64_key
                _, nick, key = data.split(":", 2)
                public_keys[nick] = key.encode("utf-8")
            else:
                sender, encrypted_msg = data.split(":", 1)
                if sender != nickname:
                    try:
                        decrypted = encryptor.decrypt(encrypted_msg.strip())
                        print(f"{sender}: {decrypted}")
                    except:
                        print(f"{sender}: (could not decrypt)")
        except :
            print("error")
            client.close()
            break

def write():
    while True:
        raw_msg = input("")
        for nick, pubkey in public_keys.items():
            if nick != nickname:
                encrypted = encryptor.encrypt(raw_msg, pubkey)
                message = f"{nickname}:{encrypted}"
                client.send(message.encode("utf-8"))




receive_thread=threading.Thread(target=receive)
receive_thread.start()
write_thread=threading.Thread(target=write)
write_thread.start()