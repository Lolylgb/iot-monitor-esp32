# Testa o sensor DHT11 isoladamente (GPIO4).
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(4))
time.sleep(2)

try:
    sensor.measure()
    print("Temperatura:", sensor.temperature(), "C")
    print("Umidade:", sensor.humidity(), "%")
except OSError as e:
    print("Erro:", e)   # ETIMEDOUT = verificar fiacao / pull-up
