# --- CONFIGURACIÓN DE CLIENTES DE STOIC ECHOES ---

CLIENTES = {
    "PRUEBA_JESUS": {
        "pixel_id": "1466581378379355",
        "access_token": "EABCbBN63ZBwcBRG48cMR8csjZCt1VVhB527ergWIPSS4PVdavxooFB1HruPMO8Bo7sCWJhWIVg9lc4iobUQUv2KXOzHowfvGnq6TmujLOhD4paZAA8b9PDb2JWzYxAKyYsKMb7ojZCvcwcHiumJB82QsSpXVy7339Lt9W5LT34ZClafDZCqhOxJTU3e77JggZDZD",
        "test_code": "TEST39997",
        "sheet_name": "Capi_test",
        "rango_filas": 2, # Desde qué fila empiezan los datos
        "col_status": 7   # Columna G (Status_Meta)
    },
    # Cuando tengas un cliente nuevo, solo copias lo de arriba aquí abajo
    "CLIENTE_DOS": {
        "pixel_id": "ID_NUEVO",
        "access_token": "TOKEN_NUEVO",
        "test_code": "TEST_NUEVO",
        "sheet_name": "HOJA_NUEVA",
        "rango_filas": 2,
        "col_status": 7
    }
}

# Aquí eliges a quién quieres procesar hoy
CLIENTE_ACTIVO = "PRUEBA_JESUS"