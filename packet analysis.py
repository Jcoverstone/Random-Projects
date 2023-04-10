from scapy.all import *

# Define a function called sniff_wireless that takes a single argument, the name of the wireless interface to sniff on
def sniff_wireless(interface):
    # Use the scapy sniff function to sniff on the specified interface
    # The 'prn' argument is a function that will be called for each packet that is sniffed
    sniff(iface=interface, prn=process_packet)

# Define a function called process_packet that takes a single argument, the packet to be processed
def process_packet(packet):
    # Check if the packet has a 802.11 layer (i.e. it is a Wi-Fi packet)
    if packet.haslayer(Dot11):
        # Get the source MAC address of the packet
        src_mac = packet[Dot11].addr2

        # Check if the packet has a layer for the Network (e.g. IP) protocol
        if packet.haslayer(IP):
            # Get the source IP address of the packet
            src_ip = packet[IP].src

            # Get the destination IP address of the packet
            dst_ip = packet[IP].dst

            # Print a message with the source MAC and IP addresses, and the destination IP address
            print(f"Wi-Fi packet from {src_mac} ({src_ip}) to {dst_ip}")