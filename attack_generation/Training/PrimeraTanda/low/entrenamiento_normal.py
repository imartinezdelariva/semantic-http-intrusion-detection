import requests
import time
import random
import string

# =============================================
# CONFIGURACION
# =============================================
BASE_URL = "http://192.168.20.10"
LOGIN_URL = f"{BASE_URL}/login.php"
CREDENCIALES = {"username": "admin", "password": "password", "Login": "Login"}
PAUSA = 0.5

# =============================================
# DATOS PARA TRAFICO NORMAL
# =============================================

NOMBRES = ["Alice", "Bob", "Carlos", "Maria", "Juan", "Pedro", "Laura",
           "David", "Ana", "Luis", "Sofia", "Miguel", "Elena", "Pablo",
           "Carmen", "Jorge", "Isabel", "Antonio", "Rosa", "Francisco"]

APELLIDOS = ["Garcia", "Martinez", "Lopez", "Sanchez", "Gonzalez", "Perez",
             "Rodriguez", "Fernandez", "Torres", "Ramirez", "Cruz", "Flores",
             "Rivera", "Morales", "Ortega", "Jimenez", "Herrera", "Medina"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/120.0.0.0 Safari/537.36",
]

URLS_NAVEGACION = [
    f"{BASE_URL}/",
    f"{BASE_URL}/index.php",
    f"{BASE_URL}/about.php",
    f"{BASE_URL}/instructions.php",
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

def generar_trafico_normal(session, n=100):
    print("\n[*] Generando trafico normal...")
    ok = 0

    for _ in range(n):
        session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        tipo = random.choice(["navegacion", "sqli_normal", "xss_normal", "brute_normal", "exec_normal"])

        try:
            if tipo == "navegacion":
                url = random.choice(URLS_NAVEGACION)
                r = session.get(url)
                print(f"  NORMAL | GET {url:<45} | status: {r.status_code}")

            elif tipo == "sqli_normal":
                id_val = str(random.randint(1, 10))
                r = session.get(f"{BASE_URL}/vulnerabilities/sqli/",
                                params={"id": id_val, "Submit": "Submit"})
                print(f"  NORMAL | SQLi id={id_val:<5} | status: {r.status_code}")

            elif tipo == "xss_normal":
                nombre = random.choice(NOMBRES)
                r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                                params={"name": nombre})
                print(f"  NORMAL | XSS nombre={nombre:<15} | status: {r.status_code}")

            elif tipo == "brute_normal":
                usuario = random.choice(NOMBRES).lower()
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 10)))
                r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                                params={"username": usuario, "password": password, "Login": "Login"})
                print(f"  NORMAL | BRUTE {usuario}:{password:<12} | status: {r.status_code}")

            elif tipo == "exec_normal":
                ip = f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
                r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                                 data={"ip": ip, "Submit": "Submit"})
                print(f"  NORMAL | EXEC ip={ip:<18} | status: {r.status_code}")

            ok += 1
            time.sleep(PAUSA)

        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"[+] Trafico normal completado: {ok}/{n} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": random.choice(USER_AGENTS)})

    print("="*60)
    print("  ENTRENAMIENTO: TRAFICO NORMAL")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'normal'")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    generar_trafico_normal(session, n=100)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'normal'")
    print("="*60)
