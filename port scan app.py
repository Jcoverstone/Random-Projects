import nmap

def scan(ip):
    # Create a new nmap PortScanner object
    scanner = nmap.PortScanner()

    # Run an nmap scan on the specified IP address, using the '-sV' option to enable version detection
    scanner.scan(ip, arguments='-sV')

    # Get the TCP ports that are open on the scanned IP address
    open_tcp_ports = []
    for port in scanner[ip]['tcp']:
        if scanner[ip]['tcp'][port]['state'] == 'open':
            open_tcp_ports.append(port)

    # Return the list of open TCP ports
    return open_tcp_ports
