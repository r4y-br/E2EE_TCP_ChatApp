import socket
import threading
from crypto_utils.rsa_encryptor import RSAEncryptor
import json
import os



encryptor=RSAEncryptor()
public_key=encryptor.get_public_key()


host = "0.0.0.0"
port = 55555
MAX_CLIENTS = 2



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
public_keys = {}









def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                pass

def handle(client):
    while True:
        try:
            message = client.recv(4096)
            if message:
                print(f"[ENCRYPTED MESSAGE]: {message.decode('utf-8')}")
                broadcast(message, sender=client)

        except:
            if client in clients:
                index = clients.index(client)
                nickname = nicknames[index]
                print(f"{nickname} disconnected.")
                clients.remove(client)
                nicknames.remove(nickname)
                del public_keys[nickname]
                broadcast(f"{nickname} left the chat.".encode('utf-8'))
                client.close()
                break
def receive():
    print("🔐 Secure chat server started.")
    while True:
        client, address = server.accept()

        if len(clients) >= MAX_CLIENTS:
            print(f"Refused connection from {address} (room full)")
            client.send("ROOM_FULL".encode("utf-8"))
            client.close()
            continue


        print(f"Connected with {str(address)}")

        client.send("nick".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        client.send("send_key".encode("utf-8"))
        public_key = client.recv(2048)

        nicknames.append(nickname)
        clients.append(client)
        public_keys[nickname] = public_key
        print(f"{nickname} joined the chat")

        # Send the new user's key to the other client
        for c in clients:
            if c != client:
                c.send(f"PUBKEY:{nickname}:{public_key.decode()}".encode("utf-8"))

        # Send existing keys to the new client
        for nick, key in public_keys.items():
            if nick != nickname:
                client.send(f"PUBKEY:{nick}:{key.decode()}".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()