import requests

URL = 'http://192.168.0.109'

def sendData(data):
    try:
        response = requests.get(URL+data)
        response_json = response.json()
        print('datos:',str(response))
        return response_json
    except:
        print("Problemas en la validacion")
        return -1
    

while True:
    n = input('Ingresa un estado del led: ')
    if(n == "on"):
        sendData("/led_on")
    elif(n == "off"):
        sendData("/led_off")
