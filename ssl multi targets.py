import socket
import ssl

class TLSScanner:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def scan(self):
        context = ssl.create_default_context()
        with socket.create_connection((self.host, self.port)) as sock:
            with context.wrap_socket(sock, server_hostname=self.host) as ssock:
                try:
                    ssock.do_handshake()
                except ssl.SSLError as e:
                    if 'CERTIFICATE_VERIFY_FAILED' in str(e):
                        print(f"{self.host}:{self.port} - Invalid SSL/TLS certificate!")
                    elif 'SSLV3_ALERT_HANDSHAKE_FAILURE' in str(e):
                        print(f"{self.host}:{self.port} - SSLv3 protocol not supported!")
                    elif 'SSLV3_ALERT_PROTOCOL_VERSION' in str(e):
                        print(f"{self.host}:{self.port} - TLS protocol not supported!")
                    else:
                        print(f"{self.host}:{self.port} - SSL/TLS connection failed: {e}")
                else:
                    print(f"{self.host}:{self.port} - SSL/TLS connection succeeded with {ssock.version()}")

if __name__ == "__main__":
    targets = [
        ("example.com", 443),
        ("test.com", 443),
        ("badssl.com", 443),
        ("expired.badssl.com", 443),
        ("self-signed.badssl.com", 443)
    ]
    
    for target in targets:
        scanner = TLSScanner(target[0], target[1])
        scanner.scan()