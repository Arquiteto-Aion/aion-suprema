from flask import Flask, request, jsonify
import geocoder
import time
import threading
from datetime import datetime

app = Flask(_name_)

# Geolocalização
class Geolocalizacao:
    def _init_(self):
        self.local = None
    
    def por_ip(self):
        g = geocoder.ip('me')
        return {'ip': g.ip, 'lat': g.latlng[0] if g.latlng else None, 'lng': g.latlng[1] if g.latlng else None}

geoloc = Geolocalizacao()

# Dead man's switch (3 dias)
ultimo_comando = datetime.now()
alerta = False

def monitorar():
    global alerta
    while True:
        tempo = (datetime.now() - ultimo_comando).total_seconds()
        if tempo > 3 * 24 * 3600 and not alerta:
            alerta = True
            print("ALERTA: Arquiteto sumiu! Buscando...")
        time.sleep(3600)

threading.Thread(target=monitorar, daemon=True).start()

@app.route('/')
def home():
    return 'AION ESTÁ VIVA!'

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/local')
def local():
    return geoloc.por_ip()

@app.route('/comando', methods=['POST'])
def comando():
    global ultimo_comando, alerta
    ultimo_comando = datetime.now()
    alerta = False
    return {'status': 'ok'}

@app.route('/status')
def status():
    dias = (datetime.now() - ultimo_comando).total_seconds() / 86400
    return {'status': 'ALERTA' if alerta else 'NORMAL', 'dias_sem_comando': round(dias, 2)}

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
