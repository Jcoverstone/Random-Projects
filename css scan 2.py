import requests

def xss_scan(target_url):
    # Test for XSS vulnerability by injecting a script tag into a form field
    # If the response contains the injected script, it may be vulnerable to XSS
    payload = "<script>alert('XSS')</script>"
    data = {'username': payload, 'password': 'test'}
    response = requests.post(target_url, data=data)
    if payload in response.text:
        print("{} may be vulnerable to XSS".format(target_url))
    else:
        print("{} is not vulnerable to XSS".format(target_url))

# Example usage:
xss_scan('https://example.com/login.php')
