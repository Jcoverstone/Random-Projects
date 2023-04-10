import requests

def lookup_mac_address(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for 4xx/5xx errors
        vendor = response.text.strip()
        return vendor
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
