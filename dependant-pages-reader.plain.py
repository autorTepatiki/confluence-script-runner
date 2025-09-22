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
    print(f"URL: {base_url}/content/{page['id']}")
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
        print("\nPage Content:", response.json())
        return response.json()
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
