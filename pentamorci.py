"""ALMACENADOR DE NUBE GIT HUB CREADO POR ANDRES"""
# esto funciona con añadir o modificar datos al {} o solo leer sus valores.

import requests
import base64
import json

url = 'https://raw.githubusercontent.com/mrmorcilla/python/refs/heads/main/texto.txt'
response = requests.get(url)
contenido = response.text
# Configuración
token = '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' # token o API
repo_owner = 'mrmorcilla'
repo_name = 'python'
file_path = 'texto.txt'
branch_name = 'main'
new_content = ''
data={}
chori=False

rspst=str(input('Quieres ver(1) editar(2) remover(3): '))
if rspst == '1':
    arc=input('nombre de archivo: ')
    exec(f'data={contenido}')
    exec(f'print(data["{arc}"])')
elif rspst == '2':
    arc=input('nombre del archivo: ')
    con=input('contenido del archivo: ')
    data[arc] = con
    new_content=str(data)
    chori=True
elif rspst == '3':
    arc=input('nombre del archivo: ')
    exec('data = contenido')
    exec(f'del data["{arc}"]')
    new_content=str(data)
    chori=True

if chori:
    # URL api, git hub
    url_get_file = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={branch_name}'

    headers = {'Authorization': f'token {token}'} # autenticacion

    response = requests.get(url_get_file, headers=headers)

    if response.status_code == 200:
        # decodificado
        file_data = response.json()
        file_content = base64.b64decode(file_data['content']).decode('utf-8')
        sha = file_data['sha']  # basicamente SHA

        print(f"Contenido actual del archivo:\n{file_content}\n")

        updated_content = new_content

        # codficiar en base64
        encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

        data = {
            "message": "Actualizar archivo desde Python",
            "content": encoded_content,
            "sha": sha
        }

        # soli
        url_update_file = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
        update_response = requests.put(url_update_file, headers=headers, data=json.dumps(data))

        if update_response.status_code == 200:
            print("Hecho")
        else:
            print(f"Error: {update_response.status_code}")
    else:
        print(f"Error de obtension: {response.status_code}")

input()
