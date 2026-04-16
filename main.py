import hashlib
import requests
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

# --- 🔑 TUS CREDENCIALES (RELLENA ESTO) ---
PIXEL_ID = "1466581378379355"
ACCESS_TOKEN = "TEABCbBN63ZBwcBREEooJzMB9MGCiGBY5A5Ma1a6Q1HO7H21AgzE8BdmrneHeiLrrlZCHXIFj8DiryloCr51WF9SkNbmIznWphul3s1SyXBSiUbZAxuhQEwYXcRhlWQseVzKWKsorglE9aiRUZCHA2ZAOBDayR4b5rhclgXe11OFI1jN33zzVLVobSJ9PIT3gZDZD"  # <--- ¡IMPORTANTE!
TEST_CODE = "TEST35244"    # <--- ¡IMPORTANTE!
SHEET_NAME = "Capi_test" 

def hash_data(data):
    if not data or data == "": return None
    return hashlib.sha256(str(data).strip().lower().encode()).hexdigest()

def send_to_meta(row):
    url = f"https://graph.facebook.com/v19.0/{PIXEL_ID}/events"
    user_data = {
        "em": [hash_data(row.get('Email'))],
        "ph": [hash_data(row.get('Teléfono'))],
        "client_ip_address": "127.0.0.1",
        "client_user_agent": "Mozilla/5.0"
    }
    payload = {
        "data": [{
            "event_name": "Purchase",
            "event_time": int(time.time()),
            "action_source": "system_offline",
            "user_data": user_data,
            "custom_data": { "value": row.get('Monto'), "currency": row.get('Moneda', 'USD') }
        }],
        "access_token": ACCESS_TOKEN,
        "test_event_code": TEST_CODE 
    }
    r = requests.post(url, json=payload)
    return r.status_code == 200

def run_sync():
    print("--- 🚀 STOIC ECHOES: MODO RADAR ACTIVADO ---")
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        
        records = sheet.get_all_records()
        print(f"📋 Filas leídas en el Excel: {len(records)}")

        for i, row in enumerate(records, start=2):
            # Limpiamos los datos para que no importen espacios o mayúsculas
            origen = str(row.get('Origen', '')).strip().upper()
            status = str(row.get('Status_Meta', '')).strip().upper()
            email = row.get('Email', 'Desconocido')

            print(f"🔍 Analizando fila {i} ({email}): Origen={origen}, Status={status}")

            if origen == "PAID" and status != "SÍ":
                print(f"📡 ¡DISPARANDO! Enviando a {email}...")
                if send_to_meta(row):
                    sheet.update_cell(i, 7, "SÍ")
                    print(f"✅ ÉXITO: {email} sincronizado.")
                else:
                    print(f"❌ ERROR: Meta rechazó el evento de {email}.")
        
        print("--- ✨ Fin de la misión ---")
    except Exception as e:
        print(f"💥 ERROR TÉCNICO: {e}")

if __name__ == "__main__":
    run_sync()