import threading
import time
import socket
import struct

UDP_IP = "127.168.0.0"
UDP_PORT = 5005
MESSAGE = "Hello, World!"
TTL = struct.pack('b', 1)
vecEntradas = {"127.168.0.1", "127.168.0.6", "127.168.0.10", "127.168.0.14", "127.168.0.17"}
vecSalidas = {"127.168.0.2", "127.168.0.5", "127.168.0.9", "127.168.0.13", "127.168.0.18"}

router1 = {1, "127.168.0.2"}
router2 = {2, "127.168.0.18"}
router3 = {3, "127.168.0.1", "127.168.0.6", "127.168.0.14", "127.168.0.17"}
router4 = {4, "127.168.0.5", "127.168.0.10"}
router5 = {5, "127.168.0.9", "127.168.0.13"}

def servidor(entrada):
    print("SERVER")
    UDP_IP = entrada
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    print("message:", MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

def cliente(entrada):
    print("CLIENT")
    UDP_IP = entrada
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)

def crearHilosServidor(entrada):
    print("crearHilos: " + entrada)
    servidor(entrada)

def crearHilosCliente(entrada):
    print("crearHilos: " + entrada)
    cliente(entrada)

for i in vecEntradas:
    print(i)
    threading.Thread(target=crearHilosCliente(i))
    threading.Thread(target=crearHilosServidor(i))

#for i in vecSalidas:
#    print(i)
#    threading.Thread(target=crearHilosCliente(i))
#    threading.Thread(target=crearHilosServidor(i))