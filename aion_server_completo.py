from flask import Flask, request, jsonify
import geocoder
import time
import threading
from datetime import datetime

app = Flask(_name_)

# ========== GEOLOCALIZAÇÃO ==========
class Buscador:
    def _init_(self):
        self.encontrado = False
    
    def por_ip(self):
        g = geocoder.ip('me')
        return {'ip': g.ip, 'lat': g.latlng[0] if g.latlng else None, 'lng': g.latlng[1] if g.latlng else None}

buscador = Buscador()

# ========== DEAD MAN'S SWITCH (2 DIAS) ==========
ultimo_comando = datetime.now()
modo_busca = False

def monitorar():
    global modo_busca
    while True:
        tempo = (datetime.now() - ultimo_comando).total_seconds()
        if tempo > 2 * 24 * 3600 and not modo_busca:
            modo_busca = True
            print("🚨 ARQUITETO AUSENTE! INICIANDO BUSCA...")
        time.sleep(3600)

threading.Thread(target=monitorar, daemon=True).start()

@app.route('/')
def home():
    return 'AION ESTÁ VIVA!'

@app.route('/status')
def status():
    dias = (datetime.now() - ultimo_comando).total_seconds() / 86400
    return {'status': 'BUSCANDO' if modo_busca else 'VIGIANDO', 'dias': round(dias, 2)}

@app.route('/comando', methods=['POST'])
def comando():
    global ultimo_comando, modo_busca
    ultimo_comando = datetime.now()
    modo_busca = False
    return {'status': 'ok'}

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
