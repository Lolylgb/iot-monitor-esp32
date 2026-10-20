# Liga e desliga o rele (GPIO13) para confirmar fiacao e logica do modulo.
from machine import Pin
import time

rele = Pin(13, Pin.OUT)

for i in range(3):
    rele.value(1)
    print("Rele LIGADO")
    time.sleep(2)
    rele.value(0)
    print("Rele DESLIGADO")
    time.sleep(2)
