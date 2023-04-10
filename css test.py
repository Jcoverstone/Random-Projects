import requests

def test_xss(url, parameter):
    payload = f"<script>alert('XSS')</script>"
    response = requests.get(url, params={parameter: payload})
    if payload in response.text:
        return True
    else:
        return False