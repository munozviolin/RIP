import threading
import socket
import struct
import time
from datetime import datetime

relojS = datetime.utcnow() #reloj que contara mientras que se ejecuta el algoritmo
contador = 1 #cantidad de veces que va ejecutandose el servidor
UDP_IP = "127.168.0.1" #direccion a partir de la que se realizara el multicast
MASK = "255.255.255.0" #mascara por defecto
UDP_PORT = 15005 #puerto requerido para la transmision multicast
TTL = struct.pack('b', 1) #tiempo de vida
vecEntradas = {"127.168.0.1", "127.168.0.6", "127.168.0.10", "127.168.0.14", "127.168.0.17"} #primer conjunto de IPs
vecSalidas = {"127.168.0.2", "127.168.0.5", "127.168.0.9", "127.168.0.13", "127.168.0.18"} #segundo conjunto de IPs
router1IPs = [" ", " ", " "] #almacenara IPs que se comunican con router 1
router2IPs = [" ", " ", " "] #almacenara IPs que se comunican con router 2
router3IPs = [" ", " ", " ", " "] #almacenara IPs que se comunican con router 3
router4IPs = [" ", " ", " "] #almacenara IPs que se comunican con router 4
router5IPs = [" ", " ", " "] #almacenara IPs que se comunican con router 5
barrier = threading.Barrier(3) #barrera para programacion con varios hilos
router3Rutas = ["192.168.0.2", "192.168.0.5", "192.168.0.13", "192.168.0.18"] #IPs por las que puede transmitir router 3
nid = [100, 101, 102, 103, 104] #id que identificara a cada hilo
listaIPCliente = ["127.168.0.1", "127.168.0.2", "127.168.0.3", "127.168.0.4", "127.168.0.5"] #IPs clientes
router1 = ['3'] #routers vecinos del router 1
router2 = ['3'] ##routers vecinos del router 2
router3 = ['1', '2', '4', '5'] #routers vecinos del router 3
router4 = ['3', '5']  #routers vecinos del router 4
router5 = ['3', '4'] #routers vecinos del router 5
tabla1 = [["10.0.1.0", "255.255.255.0", "10.0.1.1", 1]] #datos distancia 1 de router 1
tabla2 = [["10.0.3.0", "255.255.255.0", "10.0.3.1", 1]] #datos distancia 1 de router 2
tabla3 = [] #datos distancia 1 de router 3
tabla4 = [["10.0.2.0", "255.255.255.0", "10.0.2.1", 1]] #datos distancia 1 de router 4
tabla5 = [["10.0.4.0", "255.255.255.0", "10.0.4.1", 1]] #datos distancia 1 de router 5
listasocket = [] #lista de routers representados con sockets
caido = False #cuando un router se da cuenta que se cayo el router 3 se usa este booleano
holdDown = False #cuando se activa el hold timer
redRouter1 = "10.0.1.0" #red conectada a router 1
redRouter2 = "10.0.3.0" #red conectada a router 2
redRouter4 = "10.0.2.0" #red conectada a router 4
redRouter5 = "10.0.4.0" #red conectada a router 5
saltoR1 = [1, 0, 0, 0] #utilizado para calcular la cantidad de saltos entre router 1 y los otras conexiones
saltoR2 = [0, 1, 0, 0] #utilizado para calcular la cantidad de saltos entre router 2 y los otras conexiones
saltoR3 = [0, 0, 0, 0] #utilizado para calcular la cantidad de saltos entre router 3 y los otras conexiones
saltoR4 = [0, 0, 1, 0] #utilizado para calcular la cantidad de saltos entre router 4 y los otras conexiones
saltoR5 = [0, 0, 0, 1] #utilizado para calcular la cantidad de saltos entre router 5 y los otras conexiones


#Metodo que busca en tablas de router ya existentes para determinar si existen mejores rutas
#REQUIERE:
#           tabla: Tabla RIP de un determinado router
#           numRed: numero de red que se desea determinar si nueva ruta es mejor a la existente
#           numSaltos: numero de saltos para la nueva ruta
#           siguiente: direccion al siguiente equipo para llegar a la red
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

#Metodo que identifica que informacion proviene de router 3 para actualizar el numero de saltos a 16
#REQUISITOS:
#          tabla: corresponde a la tabla que va a ser actualizada
def buscarConexiones(tabla):
    global router3Rutas
    for i in tabla:
        for j in router3Rutas:
            if j in i:
                i[3] = 16


#Metodo que simulan la funcion de envio de datos de los Routers
#REQUIERE:
#           idRouterVecino: ID del router que se rrepresenta
def servidor(idRouter):
    idRouter += 1
    listaIPs = list(vecEntradas)
    listaIPs.extend(list(vecSalidas))
    global UDP_IP
    mensaje = str(idRouter)

    global listasocket
    for i in listasocket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
        sock.sendto(mensaje.encode(), (UDP_IP, i))

#Metodo que cuenta la cantidad de saltos necesarios para llegar a una red desde un router
#REQUIERE:
#           idRouterVecino: ID del router vecino por el cual debe desplazarme para avanzar
#           dirRed: direccion de red que corresponde a la red que desea ser almacenado
#           saltos: corresponde a al cantidad de saltos que una posible ruta deberia necesitar para llegar  su detino
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


#Metodo que imprime la informacion correspondiente de cada tabla de los servidores
#REQUIERE:
#           idRouter: el ID de router que es representado por el hilo
#           tabla: la tabla que corresponde a la informacion que se va a imprimir
def imprimirDatos(idRouter, tabla):
    print("\n________________________________________________\nTABLA DE ROUTER ", idRouter, ":")
    for i in tabla:
        print (i)
     #print("Router: ", idRouter, "\n Tabla:",tabla)


#Metodo que simula la operacion de RIP para cada servidor
#REQUIERE:
#           idRouter: el ID de router que es representado por el hilo
def cliente(idRouter):
    global contador
    global tabla1, tabla2, tabla3, tabla4, tabla5
    global router1IPs, router2IPs, router3IPs, router4IPs, router5IPs
    global saltoR1, saltoR2, saltoR3, saltoR4, saltoR5
    global caido, holdDown
    global listasocket
    global reloj3
    global relojS
    reloj3=datetime.utcnow()
    dir1 = " "
    dir2 = " "
    dir3 = " "
    dir4 = " "
    #print("IPCLIENTE ", listaIPCliente[idRouter])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT + idRouter))
    listasocket.append(UDP_PORT + idRouter)
    idRouter += 1
    router = {}
    if idRouter == 1:
        router = router1
    elif idRouter == 2:
        router = router2
    elif idRouter == 3:
        router = router3
    elif idRouter == 4:
        router = router4
    else:
        router = router5

    while True:
        data, addr = sock.recvfrom(1024)  # tamano buffer 1024
        direccion = list(sock.getsockname())
        a = list(addr)
        mensaje = data.decode()
        resta= relojS- reloj3
        #print(resta.total_seconds())
        if (resta.total_seconds())  > 13:
            caido = True
        #else:
        #    print(relojS -reloj3)
        if mensaje in router or caido is True:
            if idRouter == 1:
                imprimirDatos(idRouter, tabla1)
            time.sleep(.5)
            if idRouter == 2:
                imprimirDatos(idRouter, tabla2)
            time.sleep(.5)
            if idRouter == 3:
                imprimirDatos(idRouter, tabla3)
            time.sleep(.5)
            if idRouter == 4:
                imprimirDatos(idRouter, tabla4)
            time.sleep(.5)
            if idRouter == 5:
                imprimirDatos(idRouter, tabla5)
            time.sleep(.5)

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

                elif mensaje == '3':
                    reloj3 = datetime.utcnow()
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
                        if saltoR4[3] < saltos:
                            saltoR4[3] = saltos
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

    del router


#Metodo que crea y ejecuta los hilos cliente
class threadC(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID

    def run(self):
        cliente(self.thread_ID - 100)
        barrier.wait()


#Metodo que crea y ejecuta los hilos servidor
class threadS(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID

    def run(self):
        servidor(self.thread_ID - 200)


#Metodo que indica que se a realizado el tiempo de espera para el HOLDDOWN TIMER
def activarHoldDown():
    global holdDown
    holdDown = True
    print("\n---------------------------------------------------HOLD TIMER, finalizaron los 20 segundos")


#Metodo que crea los hilos que ejecutan los servidores que envian la informacion de los routes y espera 10 segundos entre ciclos
def llamarServidor():
    global contador
    global listasocket
    global relojS
    while (True):
        i = 0
        global caido
        if contador>1:
            time.sleep(10)
        print("\n************************************************\nNÚMERO DE CORRIDA DEL SERVIDOR: ", contador)
        listThread2 = []
        for x in nid:
            threadNID = threadS(x + 100)
            listThread2.append(threadNID)

        for x in listThread2:
            relojS = datetime.utcnow()
            #print(relojS)
            if contador >= 6:
                if x.thread_ID != 202:
                    x.start()
                else:
                   if contador == 6:
                       print("\n---------------------------------------------------FINALIZÓ EJECUCIÓN DEL NODO 3")
                       reloj = threading.Timer(20, activarHoldDown)
                       reloj.start()
            elif contador < 6:
                x.start()
            i += 1
        contador += 1


#Metodo main que inicializa la simulacion
def main():
    global caido
    listThread = []
    for x in nid:
        threadNID = threadC(x)
        listThread.append(threadNID)
    for x in listThread:
        x.start()
    llamarServidor()

    print("Exit\n")


if __name__ == '__main__': main()