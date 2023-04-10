import socket
import ssl


class TLSScanner:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.status = None

    def scan(self):
        context = ssl.create_default_context()
        with socket.create_connection((self.host, self.port)) as sock:
            with context.wrap_socket(sock, server_hostname=self.host) as ssock:
                try:
                    ssock.do_handshake()
                except ssl.SSLError as e:
                    if 'CERTIFICATE_VERIFY_FAILED' in str(e):
                        self.status = "Invalid SSL/TLS certificate!"
                    elif 'SSLV3_ALERT_HANDSHAKE_FAILURE' in str(e):
                        self.status = "SSLv3 protocol not supported!"
                    elif 'SSLV3_ALERT_PROTOCOL_VERSION' in str(e):
                        self.status = "TLS protocol not supported!"
                    else:
                        self.status = f"SSL/TLS connection failed: {e}"
                else:
                    self.status = f"SSL/TLS connection succeeded with {ssock.version()}"

        return self.status


def print_results(results):
    print("Results:")
    for host, port, status in results:
        print(f"{host}:{port} - {status}")


def scan_hosts(hosts):
    results = []
    for host in hosts:
        scanner = TLSScanner(host, 443)
        status = scanner.scan()
        results.append((host, scanner.port, status))
    return results


if __name__ == "__main__":
    targets = [
        ("example.com", 443),
        ("test.com", 443),
        ("badssl.com", 443),
        ("expired.badssl.com", 443),
        ("self-signed.badssl.com", 443)
    ]

    results = scan_hosts([target[0] for target in targets])
    print_results(results)