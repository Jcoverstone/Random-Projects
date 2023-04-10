import socket
import ssl
import argparse

def scan_ssl_tls(host, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    wrapped_socket = context.wrap_socket(sock, server_hostname=host)
    try:
        wrapped_socket.connect((host, port))
        print("[+] SSL/TLS connection established to {}:{}".format(host, port))
        print("[*] Cipher suite: {}".format(wrapped_socket.cipher()))
        cert = wrapped_socket.getpeercert()
        print("[*] Issuer: {}".format(cert['issuer']))
        print("[*] Valid from: {}".format(cert['notBefore']))
        print("[*] Valid until: {}".format(cert['notAfter']))
        print("[*] Subject: {}".format(cert['subject']))
        print("[*] Certificate chain:")
        for i, (cert_type, cert_data) in enumerate(cert['certificates'], start=1):
            print("[*]   Certificate {} ({}):".format(i, cert_type))
            print("[*]   Subject: {}".format(cert_data['subject']))
            print("[*]   Issuer: {}".format(cert_data['issuer']))
            print("[*]   Valid from: {}".format(cert_data['notBefore']))
            print("[*]   Valid until: {}".format(cert_data['notAfter']))
            print()
    except (ssl.SSLError, socket.timeout, ConnectionRefusedError):
        print("[-] Failed to establish SSL/TLS connection to {}:{}".format(host, port))
    finally:
        wrapped_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SSL/TLS scanner")
    parser.add_argument("host", type=str, help="target host name or IP address")
    parser.add_argument("-p", "--port", type=int, default=443, help="target port number (default: 443)")
    args = parser.parse_args()
    scan_ssl_tls(args.host, args.port)
