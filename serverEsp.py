import socket

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'Paneles Solares'
password = 'EcitySolar'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
led.value(0)

responseTxt =''

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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        
        request = conn.recv(1024)
        request = str(request)
        
        ledOn = request.find('/led_on')
        ledOff = request.find('/led_off')
        page = request.find('/page')
        
        if ledOn == 6:
            print('LED on') 
            responseTxt = 'on'
            led.value(0)
            
        elif ledOff == 6:
            print('LED off') 
            responseTxt = 'off'
            led.value(1)
            
        response = webPage(responseTxt)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except Exception as e:
        print(e)
 x