import requests
from flask import Flask, request
import datetime
import os

app = Flask(__name__)

# --- 🔑 CONFIGURACIÓN ---
# Estos son tus datos que ya sabemos que funcionan
TOKEN_TELEGRAM = "8533937861:AAGfdYy5HkipCUbily7-X3WlWCqyVioGg3g"
MI_CHAT_ID = "1245081720"
TOKEN_VERIFICACION = "StoicEchoes2026"

def enviar_alerta_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": MI_CHAT_ID, 
        "text": mensaje, 
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"DEBUG: Telegram respondió {r.status_code}")
    except Exception as e:
        print(f"DEBUG: Error enviando a Telegram: {e}")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. VERIFICACIÓN DE META (El "Apretón de manos")
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == TOKEN_VERIFICACION:
            print("✅ Webhook verificado por Meta con éxito")
            return challenge, 200
        return 'Error de token', 403

    # 2. RECEPCIÓN DE LEADS (Lo que genera dinero)
    if request.method == 'POST':
        data = request.json
        print(f"📩 Lead recibido: {data}")

        try:
            # Mensaje simplificado para asegurar que llegue
            ahora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
            mensaje_tlg = f"🔔 *¡NUEVO LEAD DETECTADO!*\n\n"
            mensaje_tlg += f"📅 *Fecha:* {ahora}\n"
            mensaje_tlg += f"🚀 *Origen:* Meta Ads\n\n"
            mensaje_tlg += "Checkea tu administrador de anuncios para ver los detalles."
            
            enviar_alerta_telegram(mensaje_tlg)
            
        except Exception as e:
            print(f"❌ Error procesando datos: {e}")

        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    # Usamos el puerto que Railway/Heroku asigne o el 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)