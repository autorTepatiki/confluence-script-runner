import requests
import os
import sys
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment configuration
base_url = 'https://mycompany.atlassian.net/wiki/rest/api'
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
base_url = 'https://tecocloud.atlassian.net/wiki/rest/api'
usermail = os.getenv('usermail')
api_token = os.getenv('api_token')
parent_page_id = os.getenv('parent_page_id')

# Changelogg string
changelog_string =  "<h1>Changelog</h1><p><a X </a></p><p /><p />"


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

# Function to get page content
def get_page_content(page):
    url = f"{base_url}/content/{page}?expand=body.storage,version,space"
    auth = HTTPBasicAuth(usermail, api_token)
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, auth=auth, headers=headers)
    # Ensure the response is handled with UTF-8 encoding
    response.encoding = 'utf-8'

    if response.status_code == 200:
        print("\nPage Content:", response.json())
        data = response.json()
        space_key = data["space"]["key"]
        space_name = data["space"]["name"]
        print(f"SPACE_KEY: {space_key}")
        print(f"Nombre del espacio: {space_name}")
        return data
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None

# Main script
def main():
    page_id = check_user_params(parent_page_id)
    print(f"Page id: {page_id}")
    try:
        # Get page content 
        datos_pagina = get_page_content(page_id)
        
        version_actual = datos_pagina["version"]["number"]
        titulo = datos_pagina["title"]

        payload = {
            "id": page_id,
            "type": "page",
            "title": titulo,
            "version": {
                "number": version_actual + 1
            },
            "body": {
                "storage": {
                    "value": changelog_string,
                    "representation": "storage"
                }
            }
        }

        url = f"{base_url}/content/{page_id}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.put(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(usermail, api_token))

        if response.status_code == 200:
            print("✅ Página actualizada correctamente.")
        else:
            print(f"❌ Error al actualizar la página: {respuesta.status_code}, {respuesta.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    print(f"Finish")

