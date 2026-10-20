# Autora: Fernanda Lorena Gonçalves Borges
#
# Monitoramento de temperatura e umidade com ESP32 + DHT11 + rele.
# - Le temperatura e umidade a cada 20 s
# - Envia os dados ao ThingSpeak
# - Aciona o rele se temperatura > 31 C OU umidade > 70 %
# - Envia alerta ao Telegram (uma vez por ocorrencia)
#
# As credenciais ficam em secrets.py (nao versionado). Veja secrets.example.py.

import network
import time
import dht
import gc
from machine import Pin
import urequests

try:
    from secrets import (SSID, SENHA, THINGSPEAK_API_KEY,
                         TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
except ImportError:
    print("secrets.py nao encontrado. Copie secrets.example.py para secrets.py e preencha.")
    raise

# ---------- PARAMETROS ----------
TEMP_LIMITE = 31        # graus Celsius
UMIDADE_LIMITE = 70     # porcentagem
INTERVALO = 20          # segundos (ThingSpeak gratuito exige >= 15 s)

# ---------- HARDWARE ----------
sensor = dht.DHT11(Pin(4))   # DHT11 no GPIO4
rele = Pin(13, Pin.OUT)      # rele no GPIO13 (ativo em nivel alto)


def url_encode(texto):
    resultado = texto.replace(' ', '%20')
    resultado = resultado.replace('!', '%21')
    resultado = resultado.replace(':', '%3A')
    resultado = resultado.replace(',', '%2C')
    return resultado


def conecta(ssid, senha):
    station = network.WLAN(network.STA_IF)

    if station.active():
        station.active(False)
        time.sleep(0.1)

    station.active(True)
    time.sleep(0.1)

    if not station.isconnected():
        print("A ligar a rede wifi...")
        station.connect(ssid, senha)

        for t in range(100):
            if station.isconnected():
                break
            time.sleep(0.1)

    if station.isconnected():
        print("Conectado com sucesso")
        print("Configuracao de rede:", station.ifconfig())
    else:
        print("Falha na ligacao. Verifique a senha ou o sinal da rede.")

    return station


def envia_thingspeak(temperatura, umidade):
    gc.collect()
    url = "http://api.thingspeak.com/update?api_key=" + THINGSPEAK_API_KEY
    url += "&field1=" + str(temperatura)
    url += "&field2=" + str(umidade)

    try:
        resposta = urequests.get(url)
        print("Enviado ao ThingSpeak:", resposta.text)
        resposta.close()
    except Exception as e:
        print("Erro ao enviar ao ThingSpeak:", e)


def envia_telegram(mensagem):
    gc.collect()
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    url += "?chat_id=" + TELEGRAM_CHAT_ID + "&text=" + url_encode(mensagem)

    try:
        resposta = urequests.get(url)
        print("Alerta enviado ao Telegram")
        resposta.close()
    except Exception as e:
        print("Erro ao enviar ao Telegram:", e)


# ---------- PROGRAMA PRINCIPAL ----------
conecta(SSID, SENHA)
time.sleep(2)

alerta_ja_enviado = False

while True:
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        umidade = sensor.humidity()

        print("Temperatura: {}C  |  Umidade: {}%".format(temperatura, umidade))

        condicao_critica = temperatura > TEMP_LIMITE or umidade > UMIDADE_LIMITE

        if condicao_critica:
            rele.value(1)
            print("Rele LIGADO")

            if not alerta_ja_enviado:
                msg = "ALERTA: Temperatura " + str(temperatura) + "C, Umidade " + str(umidade) + "%"
                envia_telegram(msg)
                alerta_ja_enviado = True
        else:
            rele.value(0)
            print("Rele DESLIGADO")
            alerta_ja_enviado = False

        envia_thingspeak(temperatura, umidade)

    except OSError as e:
        print("Erro na leitura do sensor:", e)

    time.sleep(INTERVALO)
