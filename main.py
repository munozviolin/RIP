import threading
import time
import socket
import struct
import time

UDP_IP = "127.168.0.1"
MASK = "255.255.255.0"
UDP_PORT = 15005
MESSAGE = "Hello, World!"
TTL = struct.pack('b', 1)
vecEntradas = {"127.168.0.1", "127.168.0.6", "127.168.0.10", "127.168.0.14", "127.168.0.17"}
vecSalidas = {"127.168.0.2", "127.168.0.5", "127.168.0.9", "127.168.0.13", "127.168.0.18"}
router3IPs = [" ", " ", " ", " "]
barrier = threading.Barrier(3)
nid = [100, 101, 102, 103, 104]
listaIPCliente = ["127.168.0.1", "127.168.0.2", "127.168.0.3", "127.168.0.4", "127.168.0.5"]
router1 = {'3'}
router2 = {'3'}
router3 = {'1', '2', '4', '5'}
router4 = {'3', '5'}
router5 = {'3', '4'}
tabla1 = ["10.0.1.0", "255.255.255.0", "10.0.1.1", 1]
tabla2 = ["10.0.3.0", "255.255.255.0", "10.0.3.1", 1]
tabla3 = []
tabla4 = ["10.0.2.0", "255.255.255.0", "10.0.2.1", 1]
tabla5 = ["10.0.4.0", "255.255.255.0", "10.0.4.1", 1]
listasocket = []


def servidor(idRouter):
    idRouter += 1
    # OTRA BARRERA VA ACÁ. 5 HILOS SE CREAN ACÁ
    # print("SERVER")
    # UDP_IP = entrada
    listaIPs = list(vecEntradas)
    listaIPs.extend(list(vecSalidas))
    global UDP_IP
    mensaje = str(idRouter)

    global listasocket
    for i in listasocket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
        sock.sendto(mensaje.encode(), (UDP_IP, i))
        # print(i)
    # print("IP: ",x," port: ",UDP_PORT + i)
    # print("UDP target IP:", UDP_IP)
    # print("UDP target port:", UDP_PORT+t)
    # print("message:", MESSAGE)


def cliente(idRouter):
    global tabla1
    global tabla2
    global tabla3
    global tabla4
    global tabla5
    global router3IPs
    dir1 = " "
    dir2 = " "
    dir3 = " "
    dir4 = " "
    # OTRA BARRERA VA ACÁ. 5 HILOS SE CREAN ACÁ.
    # print("CLIENT")
    print("IPCLIENTE ", listaIPCliente[idRouter])
    # UDP_IP = listaIPCliente[idRouter]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT + idRouter))
    global listasocket
    listasocket.append(UDP_PORT + idRouter)

    idRouter += 1
    router = {}
    if (idRouter == 1):
        router = router1
    elif (idRouter == 2):
        router = router2
    elif (idRouter == 3):
        router = router3
    elif (idRouter == 4):
        router = router4
    else:
        router = router5

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        direccion = list(sock.getsockname())
        # print("received addr: ", data)
        a = list(addr)
        # print("%%%% ", direccion[0])
        mensaje = data.decode()
        if mensaje in router:
            if idRouter == 5:
                print(tabla5)
                #print("YO SOY: ", idRouter)
                #print("escuché a: ", mensaje)

            if mensaje == '1'and " " in router3IPs:
                red = "10.0.1.0"
                router3IPs[0] = red
                siguiente = "192.168.0.1"
                vec = {red, MASK, siguiente, ''}
                tabla3.append(vec)
            elif mensaje == '2' and " " in router3IPs:
                red = "10.0.3.0"
                router3IPs[1] = red
                siguiente = "192.168.0.17"
                vec = {red, MASK, siguiente, ''}
                tabla3.append(vec)
            elif mensaje == '4':
                red = "10.0.2.0"
                if idRouter == 3 and " " in router3IPs:
                    siguiente = "192.168.0.6"
                    vec = {red, MASK, siguiente, ''}
                    tabla3.append(vec)

                    router3IPs[2] = red
                elif idRouter == 5:
                    siguiente = "192.168.0.9"
                    vec = {red, MASK, siguiente, ''}
                    tabla5.append(vec)
            elif mensaje == '5':
                red = "10.0.4.0"
                if idRouter == 3 and " " in router3IPs:
                    router3IPs[3] = red
                    siguiente = "192.168.0.14"
                    vec = {red, MASK, siguiente, ''}
                    tabla3.append(vec)
                elif idRouter == 4:
                    siguiente = "192.168.0.10"
                    vec = {red, MASK, siguiente, ''}
                    tabla4.append(vec)
            elif mensaje == '3':  # y comparar que router3ips.size sea menor que 4
                    if idRouter == 1:
                        siguiente = "192.168.0.2"
                        dir1 = router3IPs[1]
                        if dir1 != " ":
                            red = dir1
                            vec = {red, MASK, siguiente, ''}
                            tabla1.append(vec)

                        dir2 = router3IPs[2]
                        if dir2 != " ":
                            red = dir2
                            vec = {red, MASK, siguiente, ''}
                            tabla1.append(vec)

                        dir3 = router3IPs[3]
                        if dir3 != " ":
                            red = dir3
                            vec = {red, MASK, siguiente, ''}
                            tabla1.append(vec)
                    elif idRouter == 2:
                        siguiente = "192.168.0.18"
                        dir1 = router3IPs[0]
                        if dir1 != " ":
                            red = dir1
                            vec = {red, MASK, siguiente, ''}
                            tabla2.append(vec)

                        dir2 = router3IPs[2]
                        if dir2 != " ":
                            red = dir2
                            vec = {red, MASK, siguiente, ''}
                            tabla2.append(vec)

                        dir3 = router3IPs[3]
                        if dir3 != " ":
                            red = dir3
                            vec = {red, MASK, siguiente, ''}
                            tabla2.append(vec)
                    elif idRouter == 4:
                        siguiente = "192.168.0.5"
                        dir1 = router3IPs[0]
                        if dir1 != " ":
                            red = dir1
                            vec = {red, MASK, siguiente, ''}
                            tabla4.append(vec)

                        dir2 = router3IPs[1]
                        if dir2 != " ":
                            red = dir2
                            vec = {red, MASK, siguiente, ''}
                            tabla4.append(vec)

                    elif idRouter == 5:
                        siguiente = "192.168.0.13"
                        dir1 = router3IPs[0]
                        if dir1 != " ":
                            red = dir1
                            vec = {red, MASK, siguiente, ''}
                            tabla5.append(vec)

                        dir2 = router3IPs[1]
                        if dir2 != " ":
                            red = dir2
                            vec = {red, MASK, siguiente, ''}
                            tabla5.append(vec)

        # else:
        #   print("========", mensaje)

    del router


class threadC(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID

    def run(self):
        cliente(self.thread_ID - 100)
        barrier.wait()


class threadS(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID

    def run(self):
        servidor(self.thread_ID - 200)


def llamarServidor():
    time.sleep(2)
    listThread2 = []
    for x in nid:
        threadNID = threadS(x + 100)
        listThread2.append(threadNID)
    for x in listThread2:
        x.start()


# for i in vecEntradas:
def main():
    listThread = []
    for x in nid:
        threadNID = threadC(x)
        listThread.append(threadNID)
    for x in listThread:
        x.start()
    # barrier.wait()
    while (True):
        llamarServidor()

    print("Exit\n")


if __name__ == '__main__': main()
