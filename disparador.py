import hashlib
import requests
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

# --- 🔑 TUS CREDENCIALES (ACTUALIZA AQUÍ) ---
PIXEL_ID = "1466581378379355"
ACCESS_TOKEN = "EABCbBN63ZBwcBREEooJzMB9MGCiGBY5A5Ma1a6Q1HO7H21AgzE8BdmrneHeiLrrlZCHXIFj8DiryloCr51WF9SkNbmIznWphul3s1SyXBSiUbZAxuhQEwYXcRhlWQseVzKWKsorglE9aiRUZCHA2ZAOBDayR4b5rhclgXe11OFI1jN33zzVLVobSJ9PIT3gZDZD" 
TEST_CODE = "TEST53092" # <--- ¡Pon el nuevo que te dio Meta!
SHEET_NAME = "Capi_test" 

print("\n" + "="*40)
print("🚀 STOIC ECHOES: AJUSTE DE ACCIÓN FINAL")
print("="*40)

def hash_data(data):
    if not data or data == "": return None
    return hashlib.sha256(str(data).strip().lower().encode()).hexdigest()

try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    
    records = sheet.get_all_records()
    print(f"📊 Filas en Excel: {len(records)}")

    for i, row in enumerate(records, start=2):
        email = row.get('Email')
        origen = str(row.get('Origen', '')).strip().upper()
        status = str(row.get('Status_Meta', '')).strip().upper()

        if origen == "PAID" and status != "SÍ":
            print(f"\n📡 Enviando a Meta: {email}...")
            
            # --- ENVÍO A META (CAMBIADO A 'website' SEGÚN ERROR) ---
            url = f"https://graph.facebook.com/v11.0/{PIXEL_ID}/events"
            payload = {
                "data": [{
                    "event_name": "Purchase",
                    "event_time": int(time.time()),
                    "action_source": "website",  # <--- Esto es lo que Meta pidió
                    "user_data": {
                        "em": [hash_data(email)],
                        "ph": [hash_data(row.get('Teléfono'))],
                        "client_ip_address": "127.0.0.1",
                        "client_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                    },
                    "custom_data": { "value": float(row.get('Monto', 0)), "currency": "USD" }
                }],
                "access_token": ACCESS_TOKEN,
                "test_event_code": TEST_CODE 
            }
            
            r = requests.post(url, json=payload)
            print(f"🌎 Respuesta de Meta: {r.status_code}")
            
            if r.status_code == 200:
                print(f"✍️ Escribiendo 'SÍ' en fila {i}...")
                sheet.update_cell(i, 7, "SÍ")
                print(f"✅ GOOGLE ACTUALIZADO para {email}")
            else:
                print(f"❌ META SIGUE RECHAZANDO: {r.text}")

    print("\n" + "="*40)
    print("✨ PROCESO TERMINADO")
    print("="*40)

except Exception as e:
    print(f"\n💥 ERROR GENERAL: {e}")