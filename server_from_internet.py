#Librerias
import time
from machine import Pin
import network
import socket
#Configuración inicial de WiFi
ssid = 'Paneles Solares'  #Nombre de la Red
password = 'EcitySolar' #Contraseña de la red
wlan = network.WLAN(network.STA_IF)
wlan.active(True) #Activa el Wifi
wlan.connect(ssid, password) #Hace la conexión
while wlan.isconnected() == False: #Espera a que se conecte a la red
    pass
print('Conexion con el WiFi %s establecida' % ssid)
print(wlan.ifconfig()) #Muestra la IP y otros datos del Wi-Fi
#Salidas
cafetera = Pin(2, Pin.OUT)
cocina = Pin(5, Pin.OUT)
#Pagina web
def web_page():  
    html = """    <html>
            <head>
                <title>MicroTutoriales DC</title>
                <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <!--<meta http-equiv="refresh" content="2">-->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
            </head>
            
            <body>
                <!-- Image and text -->
                <nav class="navbar navbar-danger bg-danger">
                    <a class="navbar-brand" href="#">
                        <img src="https://microtutorialesdc.com/images/logo.png" width="250" height="30" class="d-inline-block align-top" alt="">
                        <span class="text-white">Monitoring</span>
                    </a>
                </nav>
            
                <div class="container">
                    <div class="row">
                        <div class="col-sm-12 col-md-4">
                            <div class="card" style="width: 18rem;">
                                <img src="https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.sanborns.com.mx%2Fimagenes-sanborns-ii%2F1200%2F8414234997661.jpg&f=1&nofb=1" class="card-img-top" width="500" height="300">
                                <div class="card-body">
                                    <h5 class="card-title">Cafetera</h5>
                                    <p class="card-text">El control est谩 en tus manos.</p>
                                    <a href="/cafetera=on" class="btn btn-success">ON</a>
                                    <a href="/cafetera=off" class="btn btn-danger">OFF</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-12 col-md-4">
                            <div class="card" style="width: 18rem;">
                                <img src="https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.elmueble.com%2Fmedio%2F2017%2F03%2F24%2Fcocina-abierta-al-comedor_079688cd.jpg&f=1&nofb=1" class="card-img-top" width="500" height="300">
                                <div class="card-body">
                                    <h5 class="card-title">Iluminaci贸n de Cocina</h5>
                                    <p class="card-text">El control est谩 en tus manos.</p>
                                    <a href="/cocina=on" class="btn btn-success">ON</a>
                                    <a href="/cocina=off" class="btn btn-danger">OFF</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            
                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
            </body>
            
            </html>  """
    return html
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('', 80))
tcp_socket.listen(5)

while True:
    conn, addr = tcp_socket.accept()
    print('Nueva conexion desde:  %s' % str(addr))
    request = conn.recv(1024)
    print('Solicitud = %s' % str(request))
    request = str(request)
    if request.find('/cafetera=on') == 6:
        print('Cafetera ON')
        cafetera.value(1)
    if request.find('/cafetera=off') == 6:
        print('Cafetera OFF')
        cafetera.value(0)
    if request.find('/cocina=on') == 6:
        print('Cafetera ON')
        cocina.value(1)
    if request.find('/cocina=off') == 6:
        print('Cafetera OFF')
        cocina.value(0)
    
    #Mostrar Página
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('content-type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()