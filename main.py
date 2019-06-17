import threading
import time
import socket
import struct
import time

contador = 1
UDP_IP = "127.168.0.1"
MASK = "255.255.255.0"
UDP_PORT = 15005
MESSAGE = "Hello, World!"
TTL = struct.pack('b', 1)
vecEntradas = {"127.168.0.1", "127.168.0.6", "127.168.0.10", "127.168.0.14", "127.168.0.17"}
vecSalidas = {"127.168.0.2", "127.168.0.5", "127.168.0.9", "127.168.0.13", "127.168.0.18"}
router1IPs = [" ", " ", " "]
router2IPs = [" ", " ", " "]
router3IPs = [" ", " ", " ", " "]
router4IPs = [" ", " ", " "]
router5IPs = [" ", " ", " "]
barrier = threading.Barrier(3)
router3Rutas = ["192.168.0.2", "192.168.0.5", "192.168.0.13", "192.168.0.18"]
nid = [100, 101, 102, 103, 104]
listaIPCliente = ["127.168.0.1", "127.168.0.2", "127.168.0.3", "127.168.0.4", "127.168.0.5"]
router1 = ['3']
router2 = ['3']
router3 = ['1', '2', '4', '5']
router4 = ['3', '5']
router5 = ['3', '4']
tabla1 = [["10.0.1.0", "255.255.255.0", "10.0.1.1", 1]]
tabla2 = [["10.0.3.0", "255.255.255.0", "10.0.3.1", 1]]
tabla3 = []
tabla4 = [["10.0.2.0", "255.255.255.0", "10.0.2.1", 1]]
tabla5 = [["10.0.4.0", "255.255.255.0", "10.0.4.1", 1]]
listasocket = []
caido = False
holdDown = False
redRouter1 = "10.0.1.0"
redRouter2 = "10.0.3.0"
redRouter4 = "10.0.2.0"
redRouter5 = "10.0.4.0"
saltoR1 = [1, 0, 0, 0]
saltoR2 = [0, 1, 0, 0]
saltoR3 = [0, 0, 0, 0]
saltoR4 = [0, 0, 1, 0]
saltoR5 = [0, 0, 0, 1]

def buscarEnTabla(tabla, numRed, numSaltos, siguiente):
    esMenor = False
    for i in tabla:
        if numRed in i:
            for j in i:
                if type(j) == int:
                    if numSaltos <= j or numSaltos == 16:
                        esMenor = True
            if esMenor == True:
                i[0] = numRed
                i[1] = "255.255.255.0"
                i[2] = siguiente
                i[3] = numSaltos

def buscarConexiones(tabla):
    global router3Rutas
    for i in tabla:
        for j in router3Rutas:
            if j in i:
                i[3] = 16

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

def contarSaltos(idRouterVecino, dirRed, saltos):
    global redRouter1, redRouter2, redRouter4, redRouter5, router1, router2, router3, router4, router5

    if (idRouterVecino == 1 and dirRed == redRouter1) or (idRouterVecino == 2 and dirRed == redRouter2) or (idRouterVecino == 4 and dirRed == redRouter4) or (idRouterVecino == 5 and dirRed == redRouter5):
        saltos += 1
    else:
        saltos += 1
        if idRouterVecino == 1:
            for i in router1:
                contarSaltos(i, dirRed, saltos)
        elif idRouterVecino == 2:
            for i in router2:
                contarSaltos(i, dirRed, saltos)
        elif idRouterVecino == 3:
            for i in router3:
                contarSaltos(i, dirRed, saltos)
        elif idRouterVecino == 4:
            for i in router4:
                contarSaltos(i, dirRed, saltos)
        elif idRouterVecino == 5:
            for i in router5:
                contarSaltos(i, dirRed, saltos)


def compararSaltos(tabla,rutaTabla, nuevaRuta):
    global tabla1
    global tabla2
    global tabla3
    global tabla4
    global tabla5
    for i in rutaTabla:
        if(len(i)<3):
            tamañoRutaTabla=int(i)
    for i in nuevaRuta:
        if(len(i)<3):
            tamañoNuevaRuta=int(i)

    if tamañoRutaTabla < tamañoNuevaRuta:
        if tabla==1:
            i=0
            cambio=True
            while i < len(tabla1) and cambio == True:
                if tabla1[i] == rutaTabla:
                    tabla1[i] =nuevaRuta
                    cambio=False
            i=i+1
        if tabla==2:
            i=0
            cambio=True
            while i < len(tabla2) and cambio == True:
                if tabla2[i] == rutaTabla:
                    tabla2[i] =nuevaRuta
                    cambio=False
            i = i + 1

        if tabla==1:
            i=0
            cambio=True
            while i < len(tabla3) and cambio == True:
                if tabla3[i] == rutaTabla:
                    tabla3[i] =nuevaRuta
                    cambio=False
            i = i + 1

        if tabla==1:
            i=0
            cambio=True
            while i < len(tabla4) and cambio == True:
                if tabla4[i] == rutaTabla:
                    tabla4[i] =nuevaRuta
                    cambio=False
            i = i + 1

        if tabla==1:
            i=0
            cambio=True
            while i < len(tabla5) and cambio == True:
                if tabla5[i] == rutaTabla:
                    tabla5[i] =nuevaRuta
                    cambio=False
            i = i + 1


def cliente(idRouter):
    #global saltos
    global contador
    global tabla1, tabla2, tabla3, tabla4, tabla5
    global router1IPs, router2IPs, router3IPs, router4IPs, router5IPs
    global saltoR1, saltoR2, saltoR3, saltoR4, saltoR5
    global caido, holdDown

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
        if mensaje in router or caido is True:
            if idRouter == 5:
               # print("SOY #3")
                print(tabla5)
                #print(saltoR3)
                #print("YO SOY: ", idRouter)
                #print("escuché a: ", mensaje)

            if caido is True and holdDown is True:
                if idRouter == 1 and '3' in router1:
                    router1.remove('3')
                    buscarConexiones(tabla1)
                elif idRouter == 2 and '3' in router2:
                    router2.remove('3')
                    buscarConexiones(tabla2)
                elif idRouter == 4 and '3' in router4:
                    router4.remove('3')
                    buscarConexiones(tabla4)
                elif idRouter == 5 and '3' in router5:
                    router5.remove('3')
                    buscarConexiones(tabla5)

            elif caido is False and holdDown is False:
                if mensaje == '1' and contador < 6:
                    red = "10.0.1.0"
                    siguiente = "192.168.0.1"
                    saltos = saltoR1[0] + 1
                    if saltoR3[0] < saltos:
                        saltoR3[0] = saltos
                    if router3IPs[0] == " ":
                        router3IPs[0] = red
                        vec = [red, MASK, siguiente, saltos]
                        tabla3.append(vec)
                    elif router3IPs[0] != " ":
                        buscarEnTabla(tabla3, red, saltos, siguiente)

                elif mensaje == '2' and contador < 6:
                    red = "10.0.3.0"
                    siguiente = "192.168.0.17"
                    saltos = saltoR2[1] + 1
                    if saltoR3[1] < saltos:
                        saltoR3[1] = saltos
                    if router3IPs[1] == " ":
                        router3IPs[1] = red
                        vec = [red, MASK, siguiente, saltos]
                        tabla3.append(vec)
                    elif router3IPs[1] != " ":
                        buscarEnTabla(tabla3, red, saltos, siguiente)

                elif mensaje == '4':
                    red = "10.0.2.0"
                    siguiente = "192.168.0.6"
                    saltos = saltoR4[2] + 1
                    if saltoR3[2] < saltos:
                        saltoR3[2] = saltos
                    if idRouter == 3 and contador < 6 and router3IPs[2] == " ":
                        vec = [red, MASK, siguiente, saltos]
                        tabla3.append(vec)
                        router3IPs[2] = red
                    elif router3IPs[2] != " ":
                        buscarEnTabla(tabla3, red, saltos, siguiente)

                    if idRouter == 5:
                        siguiente = "192.168.0.9"
                        saltos = saltoR4[2] + 1
                        if saltoR5[2] < saltos:
                            saltoR5[2] = saltos
                        if router5IPs[2] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla5.append(vec)
                            router5IPs[2] = red
                        elif router5IPs[2] != " ":
                            buscarEnTabla(tabla5, red, saltos, siguiente)

                elif mensaje == '5':
                    red = "10.0.4.0"
                    if idRouter == 3 and contador < 6:
                        siguiente = "192.168.0.14"
                        saltos = saltoR5[3] + 1
                        if saltoR3[3] < saltos:
                            saltoR3[3] = saltos
                        if router3IPs[3] == " ":
                            router3IPs[3] = red
                            vec = [red, MASK, siguiente, saltos]
                            tabla3.append(vec)
                        elif router3IPs[3] != " ":
                            buscarEnTabla(tabla3, red, saltos, siguiente)

                    elif idRouter == 4:
                        siguiente = "192.168.0.10"
                        saltos = saltoR5[3] + 1
                        if saltoR4[3] < saltos:
                            saltoR4[3] = saltos
                        if router4IPs[2] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla4.append(vec)
                            router4IPs[2] = red
                        elif router4IPs[2] != " ":
                            buscarEnTabla(tabla4, red, saltos, siguiente)

                elif mensaje == '3':  # y comparar que router3ips.size sea menor que 4
                    if idRouter == 1:
                        siguiente = "192.168.0.2"
                        dir1 = router3IPs[1]
                        red = dir1
                        saltos = saltoR3[1] + 1
                        if saltoR1[1] < saltos:
                            saltoR1[1] = saltos
                        if dir1 != " " and router1IPs[0] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla1.append(vec)
                            router1IPs[0] = red
                        elif router1IPs[0] != " ":
                            buscarEnTabla(tabla1, red, saltos, siguiente)

                        dir2 = router3IPs[2]
                        red = dir2
                        saltos = saltoR3[2] + 1
                        if saltoR1[2] < saltos:
                            saltoR1[2] = saltos
                        if dir2 != " " and router1IPs[1] == " ":

                            vec = [red, MASK, siguiente, saltos]
                            tabla1.append(vec)
                            router1IPs[1] = red
                        elif router1IPs[1] != " ":
                            buscarEnTabla(tabla1, red, saltos, siguiente)

                        dir3 = router3IPs[3]
                        red = dir3
                        saltos = saltoR3[3] + 1
                        if saltoR1[3] < saltos:
                            saltoR1[3] = saltos
                        if dir3 != " " and router1IPs[2] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla1.append(vec)
                            router1IPs[2] = red
                        elif router1IPs[2] != " ":
                            buscarEnTabla(tabla1, red, saltos, siguiente)

                    elif idRouter == 2:
                        siguiente = "192.168.0.18"

                        dir1 = router3IPs[0]
                        red = dir1
                        saltos = saltoR2[0] + 1
                        if saltoR2[0] < saltos:
                            saltoR2[0] = saltos
                        if dir1 != " " and " " in router2IPs:
                            vec = [red, MASK, siguiente, saltos]
                            tabla2.append(vec)
                            router2IPs[0] = red
                        elif router2IPs[0] != " ":
                            buscarEnTabla(tabla2, red, saltos, siguiente)

                        dir2 = router3IPs[2]
                        red = dir2
                        saltos = saltoR3[2] + 1
                        if saltoR2[2] < saltos:
                            saltoR2[2] = saltos
                        vec = [red, MASK, siguiente, saltos]
                        if dir2 != " " and router2IPs[1] == " ":
                            tabla2.append(vec)
                            router2IPs[1] = red
                        elif router2IPs[1] != " ":
                            buscarEnTabla(tabla2, red, saltos, siguiente)

                        dir3 = router3IPs[3]
                        red = dir3
                        saltos = saltoR3[3] + 1
                        if saltoR2[3] < saltos:
                            saltoR2[3] = saltos
                        vec = [red, MASK, siguiente, saltos]
                        if dir3 != " " and router2IPs[2] == " ":
                            tabla2.append(vec)
                            router2IPs[2] = red
                        elif router2IPs[2] != " ":
                            buscarEnTabla(tabla2, red, saltos, siguiente)

                    elif idRouter == 4:
                        siguiente = "192.168.0.5"
                        dir1 = router3IPs[0]
                        red = dir1
                        saltos = saltoR3[0] + 1
                        if saltoR4[0] < saltos:
                            saltoR4[0] = saltos
                        if dir1 != " " and router4IPs[0] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla4.append(vec)
                            router4IPs[0] = red
                        elif router4IPs[0] != " ":
                            buscarEnTabla(tabla4, red, saltos, siguiente)

                        dir2 = router3IPs[1]
                        red = dir2
                        saltos = saltoR3[1] + 1
                        if saltoR4[1] < saltos:
                            saltoR4[1] = saltos
                        if dir2 != " " and router4IPs[1] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla4.append(vec)
                            router4IPs[1] = red
                        elif router4IPs[1] != " ":
                            buscarEnTabla(tabla4, red, saltos, siguiente)

                        dir2 = router3IPs[3]
                        red = dir2
                        saltos = saltoR3[2] + 1
                        if saltoR4[2] < saltos:
                            saltoR4[2] = saltos
                        if dir2 != " " and router4IPs[1] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla4.append(vec)
                            router4IPs[2] = red
                        elif router4IPs[2] != " ":
                            buscarEnTabla(tabla4, red, saltos, siguiente)

                    elif idRouter == 5:
                        siguiente = "192.168.0.13"

                        dir1 = router3IPs[0]
                        red = dir1
                        saltos = saltoR3[0] + 1
                        if saltoR5[0] < saltos:
                            saltoR5[0] = saltos
                        if dir1 != " " and router5IPs[0] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla5.append(vec)
                            router5IPs[0] = red
                        elif router5IPs[0] != " ":
                            buscarEnTabla(tabla5, red, saltos, siguiente)

                        dir2 = router3IPs[1]
                        red = dir2
                        saltos = saltoR3[1] + 1
                        if saltoR5[1] < saltos:
                            saltoR5[1] = saltos
                        if dir2 != " " and router5IPs[1] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla5.append(vec)
                            router5IPs[1] = red
                        elif router5IPs[1] != " ":
                            buscarEnTabla(tabla5, red, saltos, siguiente)

                        dir3 = router3IPs[2]
                        red = dir3
                        saltos = saltoR3[2] + 1
                        if saltoR5[2] < saltos:
                            saltoR5[2] = saltos
                        if dir3 != " " and router5IPs[1] == " ":
                            vec = [red, MASK, siguiente, saltos]
                            tabla5.append(vec)
                            router5IPs[1] = red
                        elif router5IPs[1] != " ":
                            buscarEnTabla(tabla5, red, saltos, siguiente)

        # else:
        #   print("========", mensaje)

    del router


class threadC(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID

    def run(self):
        cliente(self.thread_ID - 100)
        ##global stopthread
        #while True:
        #    if stopthread:
        #        break
        barrier.wait()

class threadS(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID

    def run(self):
        servidor(self.thread_ID - 200)

def activarHoldDown():
    global holdDown
    holdDown = True

def llamarServidor():
    #contador=1
    #global thread3
    global contador
    global listasocket
    while (True):
        i = 0
        global caido
        time.sleep(2)
        listThread2 = []
        for x in nid:
            threadNID = threadS(x + 100)
            listThread2.append(threadNID)

        for x in listThread2:
            if contador >= 6:
                if x.thread_ID != 202:
                    x.start()
                else:
                    caido = True
                    reloj = threading.Timer(20, activarHoldDown())
                    reloj.start()
                #else:
                #    stopthread = True
                #    thread3[0].join()
            elif contador < 6:
                x.start()
            i += 1

        contador += 1
        print("contador: ",contador)


# for i in vecEntradas:
def main():
    #buscarEnTabla(tablaPrueba, '10.0.3.0', 4, '192.168.0.5')
    #print(tablaPrueba)

    global caido
    listThread = []
    for x in nid:
        threadNID = threadC(x)
        listThread.append(threadNID)
        #if nid==102:
        #    global thread3
        #    thread3.append(threadNID)

    for x in listThread:
        x.start()
    # barrier.wait()
    #while (True):
    llamarServidor()
    #time.sleep(300)

    print("Exit\n")


if __name__ == '__main__': main()