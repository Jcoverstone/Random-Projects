import requests

def sql_injection_scan(target_url):
    # Test for SQL injection vulnerability by appending a single-quote to the URL
    # If the response contains a database error message, it may be vulnerable to SQL injection
    url = target_url + "'"
    response = requests.get(url)
    if "SQL syntax" in response.text:
        print("{} may be vulnerable to SQL injection".format(target_url))
    else:
        print("{} is not vulnerable to SQL injection".format(target_url))

# Example usage:
sql_injection_scan('https://example.com/login.php')
