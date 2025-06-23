# E2EE TCP Chat App

A simple **end-to-end encrypted** real-time chat application built in Python using raw TCP sockets and RSA encryption.

---

## 🔐 Project Overview

This project demonstrates a secure chat system where:

- Each client generates an **RSA key pair (2048-bit)**
- Clients exchange **public keys** when connecting
- Messages are **encrypted using the recipient’s public key**
- The server acts as a **blind relay**, forwarding only encrypted messages and **cannot decrypt user messages**
- Supports up to **2 clients per room**
- Fully implemented with Python’s `socket` and `threading` modules
- Command-line interface (CLI) based

---

## ⚙️ Features

- End-to-end encryption (E2EE) with RSA + OAEP padding
- Public key exchange and management
- Secure message broadcasting between clients
- Modular `RSAEncryptor` class for encryption/decryption and key management
- Basic client authentication by nickname and public key
- Graceful handling of client disconnects
- Limits max clients per room (default 2)

---

## 🛠️ Getting Started

### Requirements

- Python 3.7+
- [pycryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)

Running the server
```bash
python server.py
```

Running the client
```bash
python client.py
```
Then enter your nickname when prompted.

## 📁 Project Structure
````bash
.
├── client.py              # Client-side chat app
├── server.py              # Server-side relay with client management
├── crypto_utils/
│   └── rsa_encryptor.py   # RSAEncryptor class for key management & crypto
├── README.md              # This file
└── .gitignore             # Git ignore rules
````

## 🚀 Next Steps / Improvements
-Implement user authentication with passwords and digital signatures

-Support multiple chat rooms and more than 2 clients

-Add a graphical or web frontend using WebSockets

-Enhance security by verifying public keys and mitigating replay attacks

-Store user data securely (e.g., encrypted database)


## 👨‍💻 About Me
I'm exploring secure communication and cryptography by building fun projects in Python.
Follow me for more updates on cybersecurity and programming.

🔗 [GitHub Repo](https://github.com/r4y-br)
