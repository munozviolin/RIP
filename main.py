import threading
import time
import socket
import struct

UDP_IP = "127.168.0.0"
UDP_PORT = 15005
MESSAGE = "Hello, World!"
TTL = struct.pack('b', 1)
vecEntradas = {"127.168.0.1", "127.168.0.6", "127.168.0.10", "127.168.0.14", "127.168.0.17"}
vecSalidas = {"127.168.0.2", "127.168.0.5", "127.168.0.9", "127.168.0.13", "127.168.0.18"}
entrada = "127.168.0.1"
barrier = threading.Barrier(3)#
# contador = 0
#nid0 = 100
#nid1 = 101
#nid2 = 102
#nid3 = 103
#nid4 = 104
nid = [100, 101, 102, 103, 104]
router1 = {1, "127.168.0.2"}
router2 = {2, "127.168.0.18"}
router3 = {3, "127.168.0.1", "127.168.0.6", "127.168.0.14", "127.168.0.17"}
router4 = {4, "127.168.0.5", "127.168.0.10"}
router5 = {5, "127.168.0.9", "127.168.0.13"}


def servidor(entrada,t):
    #OTRA BARRERA VA ACÁ. 5 HILOS SE CREAN ACÁ
    #print("SERVER")
    #UDP_IP = entrada
    listaIPs = list(vecEntradas)
    listaIPs.extend(list(vecSalidas))
    for x in listaIPs:
        for i in range(4):
            UDP_IP = x
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
            sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT + i))
    #print("UDP target IP:", UDP_IP)
    #print("UDP target port:", UDP_PORT+t)
    #print("message:", MESSAGE)




def cliente(entrada ,idRouter):
    # OTRA BARRERA VA ACÁ. 5 HILOS SE CREAN ACÁ.
    #print("CLIENT")
    #print(UDP_PORT + idRouter)
    UDP_IP = entrada
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT + idRouter))
    router={}
    if(idRouter == 0):
        router = list(router1)
    if (idRouter == 1):
        router = list(router2)
    if (idRouter == 2):
        router = list(router3)
    if (idRouter == 3):
        router = list(router4)
    if (idRouter == 4):
        router = list(router5)

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        direccion=list(sock.getsockname())
        #print("received addr:", addr[0])
        a=list(addr)
        print (a[0])
        if( direccion[0] in router):
            print("received message:", data)
    del router

class threadC(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        cliente(entrada , self.thread_ID-100)
        barrier.wait()

class threadS(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        servidor(entrada, self.thread_ID-200)

# for i in vecEntradas:
def main():
    listThread=[]
    for x in nid:
        threadNID = threadC(x)
        listThread.append(threadNID)
    for x in listThread:
        x.start()
       # barrier.wait()

    listThread2 = []
    for x in nid:
        threadNID = threadS(x+100)
        listThread2.append(threadNID)
    for x in listThread2:
        x.start()


    print("Exit\n")

if __name__ == '__main__': main()
