import hashlib
import requests
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from config import CLIENTES, CLIENTE_ACTIVO # Importamos tu configuración

# Cargamos los datos del cliente elegido
cfg = CLIENTES[CLIENTE_ACTIVO]

print(f"\n🚀 STOIC ECHOES: PROCESANDO A [{CLIENTE_ACTIVO}]")
print("-" * 40)

def hash_data(data):
    if not data or data == "": return None
    return hashlib.sha256(str(data).strip().lower().encode()).hexdigest()

try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(cfg['sheet_name']).sheet1
    
    records = sheet.get_all_records()
    print(f"📊 Datos cargados. Filas encontradas: {len(records)}")

    for i, row in enumerate(records, start=cfg['rango_filas']):
        origen = str(row.get('Origen', '')).strip().upper()
        status = str(row.get('Status_Meta', '')).strip().upper()
        email = row.get('Email', 'Sin Email')

        if origen == "PAID" and status != "SÍ":
            print(f"📡 Enviando a Meta: {email}...")
            
# --- ENVÍO A META ---
            url = f"https://graph.facebook.com/v11.0/{cfg['pixel_id']}/events"
            
            # Definimos el paquete básico (sin el código de prueba)
            payload = {
                "data": [{
                    "event_name": "Purchase",
                    "event_time": int(time.time()),
                    "action_source": "website",
                    "user_data": {
                        "em": [hash_data(email)],
                        "ph": [hash_data(row.get('Teléfono'))],
                        "client_ip_address": "127.0.0.1",
                        "client_user_agent": "Mozilla/5.0"
                    },
                    "custom_data": {
                        "value": float(row.get('Monto', 0)),
                        "currency": "USD"
                    }
                }],
                "access_token": cfg['access_token']
            }

            # 💡 AQUÍ LA MAGIA: Si hay un test_code en config.py, lo agregamos al paquete
            if cfg.get('test_code') and cfg['test_code'] != "":
                payload["test_event_code"] = cfg['test_code']
            
            # Ahora enviamos el paquete (con o sin test_code, según sea el caso)
            r = requests.post(url, json=payload)
            
            
            
            if r.status_code == 200:
                sheet.update_cell(i, cfg['col_status'], "SÍ")
                print(f"✅ ¡ÉXITO! {email} marcado en Google.")
            else:
                print(f"❌ ERROR META: {r.text}")

except Exception as e:
    print(f"💥 ERROR SISTEMA: {e}")

print("-" * 40)
print("✨ LÍNEA DE MONTAJE FINALIZADA\n")