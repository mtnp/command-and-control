# Imports
from ctypes.wintypes import INT
from getpass import getpass
import socket
import subprocess

# Setting Up IP/Sockets
REMOTE_HOST = '10.0.2.5'
REMOTE_PORT = 4444
client = socket.socket()

# Initializing Connection
print("[-] Connection Initiating...")
client.connect((REMOTE_HOST, REMOTE_PORT))
print("[-] Connection initiated!")


password = getpass()
client.send(password.encode())

# Runtime Loop
while True:
        command = input('Enter Command: ')
        while command == '':
                command = input('Enter Command: ')

        command = command.encode()

        client.send(command)

        if command == b'exit':
                break

        output = client.recv(1024)
        output = output.decode()
        if output == 'no stdout':
                print()
        else:
                print(output)

client.close()
