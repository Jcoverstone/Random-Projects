import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for 4xx/5xx errors
        soup = BeautifulSoup(response.content, "html.parser")
        content = ""

        for script in soup(["script", "style"]):
            script.decompose() # Remove script and style tags

        for text in soup.stripped_strings:
            content += text + " "

        return content
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None