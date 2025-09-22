import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Replace these variables with your Confluence instance details
CONFLUENCE_URL = 'https://tecocloud.atlassian.net/wiki/rest/api/content/'
USERMAIL = os.getenv('usermail')
API_TOKEN = os.getenv('api_token')
PAGE_ID = os.getenv('page_id')

def get_confluence_page(page_id):
    url = f"{CONFLUENCE_URL}{page_id}"
    auth = HTTPBasicAuth(USERMAIL, API_TOKEN)
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, auth=auth, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None

def main():
    page_content = get_confluence_page(PAGE_ID)
    if page_content:
        print("\nPage Content:", page_content)
        print("\nPage Title:", page_content['title'])
        print("\nPage Links:", page_content['_links'])
        ## print("Page Content:", page_content['body']['storage']['value'])

if __name__ == "__main__":
    main()
