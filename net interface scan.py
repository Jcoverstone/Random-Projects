import pcap
import sys

def handle_packet(packet):
    # Analyze the packet for information
    # ...

    # Print a summary of the information found
    # ...
    print(packet)

def scan_network_interface(dev):
    # Open the network interface for capturing
    handle = pcap.pcap(dev, timeout_ms=1000)

    # Capture network packets and analyze them
    try:
        while True:
            packet = handle.next()
            handle_packet(packet)
    except KeyboardInterrupt:
        # Cleanup
        handle.close()

# Example usage
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python sniffer.py [network interface]')
        sys.exit(1)
    scan_network_interface(sys.argv[1])