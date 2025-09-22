import requests
import os
import sys
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from datetime import datetime
from datetime import date

# Load environment variables from .env file
load_dotenv()

# Environment configuration
base_url = 'https://tecocloud.atlassian.net/wiki/rest/api'
usermail = os.getenv('usermail')
api_token = os.getenv('api_token')
parent_page_id = os.getenv('parent_page_id')

import requests
import os
import sys
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment configuration
base_url = 'https://tecocloud.atlassian.net/wiki/rest/api/content/'
usermail = os.getenv('usermail')
api_token = os.getenv('api_token')
parent_page_id = os.getenv('parent_page_id')


def check_user_params(page):    
    # Overwritten by arguments, eventually
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:], start=1):  # Excluye el nombre del script (sys.argv[0])
            print(f"User-param {i}: {arg}")
            page = arg
    else:
        print("No user-params, taking environment config file instead")

    print(f"Usermail: {usermail}")
    print(f"Page id: {page}")
    return page


# Main script
def main():
    page_id = check_user_params(parent_page_id)

    # Obtener fecha del sistema
    hoy = date.today()
    # Acceder a las partes
    yyyy = str(hoy.year)   # "2025"
    mm  = str(hoy.month)  # "8"
    dd  = str(hoy.day)    # "29"

    # Datos de la nueva página
    titulo_pagina = "Página creada para Logging"
    contenido_html = "<p>Este es el contenido de la página creada para Logging.</p>"

    # Endpoint de Confluence para crear contenido
    url = base_url
    print(url)

    # Cuerpo de la petición
    data = {
        "type": "page",
        "title": titulo_pagina + "[" + yyyy + "-" + mm + "-" + dd + "]",
        "space": {"key": "F"},
        "ancestors": [{"id": page_id}],  # Ancestro o padre
        "body": {
            "storage": {
                "value": contenido_html,
                "representation": "storage"
            }
        }
    }

    # Llamada HTTP
    response = requests.post(
        url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        auth=(usermail, api_token)
    )
    if response.status_code in (200, 201):
       print("✅ Página concatenada correctamente.")
    else:
       print("Error al crear la subpágina:", response.status_code, response.text)


if __name__ == "__main__":
    main()
    print(f"Finish")
