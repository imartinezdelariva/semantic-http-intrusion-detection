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

=============================================
# DATOS PARA TRAFICO NORMAL EVALUACION
# =============================================

NOMBRES_EVAL = ["Lucia", "Marcos", "Valeria", "Andres", "Natalia",
                "Roberto", "Patricia", "Sergio", "Monica", "Rafael",
                "Beatriz", "Alejandro", "Silvia", "Fernando", "Cristina"]

USER_AGENTS_EVAL = [
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/121.0.0.0 Mobile Safari/537.36",
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

def generar_trafico_normal_eval(session, n=50):
    print("\n[*] Generando trafico normal de evaluacion...")
    ok = 0

    for _ in range(n):
        session.headers.update({"User-Agent": random.choice(USER_AGENTS_EVAL)})
        tipo = random.choice(["navegacion", "sqli_normal", "xss_normal", "brute_normal", "exec_normal"])

        try:
            if tipo == "navegacion":
                url = random.choice(URLS_NAVEGACION)
                r = session.get(url)
                print(f"  NORMAL_EVAL | GET {url:<45} | status: {r.status_code}")

            elif tipo == "sqli_normal":
                id_val = str(random.randint(1, 10))
                r = session.get(f"{BASE_URL}/vulnerabilities/sqli/",
                                params={"id": id_val, "Submit": "Submit"})
                print(f"  NORMAL_EVAL | SQLi id={id_val:<5} | status: {r.status_code}")

            elif tipo == "xss_normal":
                nombre = random.choice(NOMBRES_EVAL)
                r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                                params={"name": nombre})
                print(f"  NORMAL_EVAL | XSS nombre={nombre:<15} | status: {r.status_code}")

            elif tipo == "brute_normal":
                usuario = random.choice(NOMBRES_EVAL).lower()
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 10)))
                r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                                params={"username": usuario, "password": password, "Login": "Login"})
                print(f"  NORMAL_EVAL | BRUTE {usuario}:{password:<12} | status: {r.status_code}")

            elif tipo == "exec_normal":
                ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                                 data={"ip": ip, "Submit": "Submit"})
                print(f"  NORMAL_EVAL | EXEC ip={ip:<18} | status: {r.status_code}")

            ok += 1
            time.sleep(PAUSA)

        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"[+] Trafico normal evaluacion completado: {ok}/{n} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": random.choice(USER_AGENTS_EVAL)})

    print("="*60)
    print("  EVALUACION: TRAFICO NORMAL")
    print("  Target: " + BASE_URL)
    print("  Etiqueta real: 'normal'")
    print("")
    print("  !! IMPORTANTE !!")
    print("  NO subir el pcap a Elasticsearch.")
    print("  Guardarlo como: evaluacion_normal.pcap")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    generar_trafico_normal_eval(session, n=50)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump y guarda el pcap como:")
    print("  evaluacion_normal.pcap")
    print("="*60)
