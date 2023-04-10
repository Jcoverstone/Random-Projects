import requests
from bs4 import BeautifulSoup
import re

def scan_website(url):
    # Retrieve website content
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Check for SQL injection vulnerability
    sql_pattern = re.compile(r"'.*?'|\d+")
    forms = soup.find_all('form')
    for form in forms:
        action = form.get('action')
        if action:
            form_url = url + action if action.startswith('/') else action
            inputs = form.find_all('input')
            for input in inputs:
                name = input.get('name')
                if name:
                    payloads = ["' or 1=1", "'; DROP TABLE users;", "' UNION SELECT * FROM users;"]
                    for payload in payloads:
                        data = {name: payload}
                        res = requests.post(form_url, data=data)
                        if re.search("You have an error in your SQL syntax", res.text):
                            print(f"SQL injection vulnerability found in {form_url}")

    # Check for cross-site scripting vulnerability
    script_pattern = re.compile(r'<script>.*</script>')
    match = script_pattern.search(r.text)
    if match:
        print("Cross-site scripting vulnerability found")

    # Check for file inclusion vulnerability
    include_pattern = re.compile(r'include\s*\(')
    match = include_pattern.search(r.text)
    if match:
        print("File inclusion vulnerability found")
