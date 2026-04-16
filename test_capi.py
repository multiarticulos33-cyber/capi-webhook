import gspread
from oauth2client.service_account import ServiceAccountCredentials

print("--- 🚀 PROBANDO CONEXIÓN DIRECTA ---")

try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Capi_test").sheet1
    
    dato = sheet.acell('A2').value
    print(f"✅ ¡Conexión exitosa! El primer dato del Excel es: {dato}")
    print("Si ves esto, la tubería está abierta. Ahora podemos correr el grande.")

except Exception as e:
    print(f"💥 Error: {e}")