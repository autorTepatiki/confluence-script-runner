import requests
import os
import sys
from bs4 import BeautifulSoup
from fpdf import FPDF
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment configuration
base_url = 'https://tecocloud.atlassian.net/wiki/rest/api'
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

# Function to get child pages
def get_child_pages(parent_id):
    url = f"{base_url}/content/{parent_id}/child/page"
    response = requests.get(url, auth=(usermail, api_token))
    response.raise_for_status()
    return response.json()

# Function to print page details
def print_page_details(page):
    print(f"Title: {page['title']}")
    print(f"URL: {base_url}/content/{page['id']}?expand=body.storage")
    print()

# Function to print page content
def print_page_content(page):
    url = f"{base_url}/content/{page['id']}"
    auth = HTTPBasicAuth(usermail, api_token)
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, auth=auth, headers=headers)
    # Ensure the response is handled with UTF-8 encoding
    response.encoding = 'utf-8'

    if response.status_code == 200:
        page_data = response.json()
        
        print("\nPage Content:", page_data)
        title = page_data['title']

        expandable = page_data['_expandable']
        if expandable == "":
            return page_data;

        print("\nExpandable:", expandable)

        body = page_data['_expandable']['body']
        if body == "":
            return page_data;
    
        print("\nBody:", body)

        storage = page_data['_expandable']['body']['storage']
        if storage == "":
            return page_data;
    
        print("\nStorage:", storage)

        content = page_data['_expandable']['body']['storage']['value']

        # Parsear el contenido HTML
        print("\nHTML parser...")
        soup = BeautifulSoup(content, 'html.parser')

        # Crear el PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font('Arial', size=12)
        print("\nGenerating PDF...")

        # Agregar el contenido al PDF
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img']):
            if element.name == 'img':
                img_url = element['src']
                img_response = requests.get(img_url, stream=True)
                img_response.raw.decode_content = True
                pdf.image(img_response.raw, x=10, y=pdf.get_y(), w=100)
                pdf.ln(10)
            else:
                pdf.multi_cell(0, 10, element.get_text())

        # Guardar el PDF
        pdf.output(f"{title}" + ".pdf")

        
        print(f"✅ PDF generado: {title}")
        return page_data;
    else:
        print(f"❌ Failed to retrieve page: {response.status_code}")
        return None

# Main script
def main():
    page_id = check_user_params(parent_page_id)
    print(f"Page id: {page_id}")
    try:
        # Get child pages of the parent page
        child_pages = get_child_pages(page_id)
        for page in child_pages['results']:
            print_page_details(page)
            # Recursively get and print details of child pages
            sub_child_pages = get_child_pages(page['id'])
            for sub_page in sub_child_pages['results']:
                print_page_details(sub_page)
                print_page_content(sub_page)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
    print(f"✅ Finish")
