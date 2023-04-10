import asyncio
import ipaddress

async def scan_port(ip_addr, port, timeout):
    """
    Scans a single port on a given IP address.

    Args:
        ip_addr (str): The IP address to scan.
        port (int): The port number to scan.
        timeout (float): The maximum time to wait for a connection (in seconds).

    Returns:
        None
    """
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip_addr, port), timeout=timeout)
        print(f"Port {port} is open on {ip_addr}")
        writer.close()
    except (asyncio.TimeoutError, ConnectionRefusedError):
        pass

async def scan_range(ip_range, port_range, timeout):
    """
    Scans a range of IP addresses and port numbers.

    Args:
        ip_range (str): The IP range to scan (in CIDR notation).
        port_range (str): The port range to scan (in the format "start-end").
        timeout (float): The maximum time to wait for a connection (in seconds).

    Returns:
        None
    """
    ip_network = ipaddress.ip_network(ip_range)
    tasks = []
    for ip in ip_network.hosts():
        for port in range(*map(int, port_range.split('-'))):
            tasks.append(asyncio.create_task(scan_port(str(ip), port, timeout)))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    ip_range = "192.168.1.1/24"
    port_range = "1-1000"
    timeout = 2

    asyncio.run(scan_range(ip_range, port_range, timeout))