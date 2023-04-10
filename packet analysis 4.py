import socket
import struct
import binascii

# Set the network interface to be sniffed
interface = 'en0'

# Create a raw socket to capture network packets
sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

# Define a function to process each captured packet
def process_packet(packet):
    # Extract the Ethernet header from the packet
    eth_header = packet[:14]
    
    # Unpack the Ethernet header fields using the struct module
    eth_fields = struct.unpack('!6s6sH', eth_header)
    
    # Extract the source and destination MAC addresses from the Ethernet header
    src_mac = binascii.hexlify(eth_fields[0]).decode('utf-8')
    dst_mac = binascii.hexlify(eth_fields[1]).decode('utf-8')
    
    # Extract the packet payload (i.e. the data beyond the Ethernet header)
    payload = packet[14:]
    
    # Print a message with the source and destination MAC addresses, and the payload of the packet
    print(f"Ethernet packet from {src_mac} to {dst_mac}: {binascii.hexlify(payload).decode('utf-8')}")

# Continuously capture and process network packets
while True:
    packet, _ = sock.recvfrom(65535)
    process_packet(packet)
