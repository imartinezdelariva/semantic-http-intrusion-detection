import requests
import time
import random
import string

BASE_URL = "http://192.168.20.10"
LOGIN_URL = f"{BASE_URL}/login.php"
CREDENCIALES = {"username": "admin", "password": "password", "Login": "Login"}
PAUSA = 0.5

# Nombres distintos a todos los scripts normal anteriores
NOMBRES_EVAL = ["Akira", "Hana", "Riku", "Sakura", "Taro",
                "Nadia", "Ivan", "Sofia", "Marco", "Elena",
                "Ali", "Fatou", "Kofi", "Amara", "Yaw"]

USER_AGENTS_EVAL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Linux; Android 14; OnePlus 12) AppleWebKit/537.36 Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
]

URLS_NAVEGACION = [
    f"{BASE_URL}/",
    f"{BASE_URL}/index.php",
    f"{BASE_URL}/about.php",
    f"{BASE_URL}/instructions.php",
    f"{BASE_URL}/security.php",
]

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

def generar_trafico_normal_eval_high(session, n=50):
    print("\n[*] Generando trafico normal HIGH (evaluacion)...")
    ok = 0
    for _ in range(n):
        session.headers.update({"User-Agent": random.choice(USER_AGENTS_EVAL)})
        tipo = random.choice(["navegacion", "sqli_normal", "xss_normal", "brute_normal", "exec_normal"])
        try:
            if tipo == "navegacion":
                url = random.choice(URLS_NAVEGACION)
                r = session.get(url)
                print(f"  NORMAL_EVAL_H | GET {url:<40} | status: {r.status_code}")

            elif tipo == "sqli_normal":
                r_get = session.get(f"{BASE_URL}/vulnerabilities/sqli/")
                token = None
                for line in r_get.text.split('\n'):
                    if 'user_token' in line and 'value' in line:
                        try:
                            token = line.split('value=')[1].split("'")[1]
                            break
                        except:
                            pass
                id_val = str(random.randint(1, 10))
                data = {"id": id_val, "Submit": "Submit"}
                if token:
                    data["user_token"] = token
                r = session.post(f"{BASE_URL}/vulnerabilities/sqli/", data=data)
                print(f"  NORMAL_EVAL_H | SQLi id={id_val} | status: {r.status_code}")

            elif tipo == "xss_normal":
                nombre = random.choice(NOMBRES_EVAL)
                r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                                params={"name": nombre})
                print(f"  NORMAL_EVAL_H | XSS nombre={nombre:<15} | status: {r.status_code}")

            elif tipo == "brute_normal":
                usuario = random.choice(NOMBRES_EVAL).lower()
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 14)))
                r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                                params={"username": usuario, "password": password, "Login": "Login"})
                print(f"  NORMAL_EVAL_H | BRUTE {usuario}:{password:<16} | status: {r.status_code}")

            elif tipo == "exec_normal":
                ip = f"127.0.{random.randint(0,1)}.{random.randint(0,10)}"
                r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                                 data={"ip": ip, "Submit": "Submit"})
                print(f"  NORMAL_EVAL_H | EXEC ip={ip:<18} | status: {r.status_code}")

            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Trafico normal High evaluacion completado: {ok}/{n} peticiones")

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": random.choice(USER_AGENTS_EVAL)})
    print("="*60)
    print("  EVALUACION: TRAFICO NORMAL — NIVEL HIGH")
    print("  Etiqueta real: 'normal'")
    print("  !! NO subir el pcap a Elasticsearch !!")
    print("  Guardarlo como: evaluacion_normal_high.pcap")
    print("  AVISO: Asegurate de que DVWA esta en nivel HIGH")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")
    if not login(session):
        exit(1)
    generar_trafico_normal_eval_high(session, n=50)
    print("\n" + "="*60)
    print("  COMPLETADO. Guarda el pcap como: evaluacion_normal_high.pcap")
    print("="*60)
