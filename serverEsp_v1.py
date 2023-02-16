import network
import socket
import time
import machine
import ujson

state = ""
led = machine.Pin(2,machine.Pin.OUT)
#Configuración inicial de WiFi
ssid = 'Paneles Solares'  #Nombre de la Red
password = 'EcitySolar' #Contraseña de la red
wlan = network.WLAN(network.STA_IF)

#wlan.active(True) #Activa el Wifi

wlan.active(False)
time.sleep(0.5)
wlan.active(True)

wlan.connect(ssid, password) #Hace la conexión
while wlan.isconnected() == False: #Espera a que se conecte a la red
    pass
print('Conexion con el WiFi %s establecida' % ssid)
print(wlan.ifconfig())

addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(addr)
server.listen(5)
print('puerto',addr)

def webPage(data="--"):  
    html = """    <html>
            <head>
                <title>MicroTutoriales DC</title>
                <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <meta http-equiv="refresh" content="2">
            </head>
            
            <body>
                <h1>Led State:  %s </h1>
            </body>
            
            </html>  """%data
    return html

while True:
    con, addr = server.accept()
    print('cliente conectado desde',addr)
    request = con.recv(1024)
    #print('Solicitud = %s' % str(request))
    request = str(request)
    
    if request.find('/led=on') == 6:
        led.value(0)
        state = "ON"
        
    if request.find('/led=off') == 6: 
        led.value(1)
        state = "OFF"
        
    if request.find('/page') == 6:
        pageRes = webPage(state)
        
        con.send('HTTP/1.1 200 OK\n')
        con.send('content-type: text/html\n')
        con.send('Connection: close \n\n')
        con.sendall(pageRes)	
    con.close()
    



















