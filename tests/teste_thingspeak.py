# Envia valores fixos ao ThingSpeak. Resposta esperada: um numero (ID da entrada).
# Execute depois que o WiFi estiver conectado (rode o main.py ou conecte antes).
import network
import time
import urequests
import gc
from secrets import SSID, SENHA, THINGSPEAK_API_KEY

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
if not wifi.isconnected():
    wifi.connect(SSID, SENHA)
    for _ in range(100):
        if wifi.isconnected():
            break
        time.sleep(0.1)
time.sleep(2)
gc.collect()

url = "http://api.thingspeak.com/update?api_key=" + THINGSPEAK_API_KEY + "&field1=25&field2=50"
try:
    r = urequests.get(url)
    print("Resposta:", r.text)
    r.close()
except Exception as e:
    print("Erro:", e)
