# Envia uma mensagem de teste pelo bot do Telegram.
import network
import time
import urequests
import gc
from secrets import SSID, SENHA, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

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

texto = "Teste%20de%20alerta%20funcionando%21"
url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage?chat_id=" + TELEGRAM_CHAT_ID + "&text=" + texto
try:
    r = urequests.get(url)
    print(r.text)   # esperado: {"ok":true,...}
    r.close()
except Exception as e:
    print("Erro:", e)
