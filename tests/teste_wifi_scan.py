# Lista as redes WiFi visiveis. Se vier vazio (0), o radio nao esta funcionando.
import network
import time

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
time.sleep(1)

redes = wifi.scan()
print("Redes encontradas:", len(redes))
for r in redes:
    print(r[0].decode(), "| canal", r[2], "| RSSI", r[3])
