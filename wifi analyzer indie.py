#!/usr/bin/env python3

import os
import sys
import time
import datetime
import argparse
import netifaces
import requests
import ipaddress
from scapy.all import *


def scan_network(interface, target_ip=None, timeout=5):
    """
    Scans the network for available hosts.

    :param interface: The network interface to use.
    :param target_ip: The target IP address or range (e.g. '192.168.0.1/24').
    :param timeout: The timeout for waiting for responses (in seconds).
    :return: A list of dictionaries containing information about the available hosts.
    """

    print(f"Scanning network using interface {interface}...")

    if not target_ip:
        # Get IP address and subnet mask for the specified interface
        addrs = netifaces.ifaddresses(interface)
        ip_address = addrs[netifaces.AF_INET][0]['addr']
        netmask = addrs[netifaces.AF_INET][0]['netmask']
        network = ipaddress.IPv4Network(f"{ip_address}/{netmask}", strict=False)

        # Construct target IP address range based on the network address and mask
        target_ip = f"{str(network.network_address)}/{network.prefixlen}"

    # Send ARP broadcast to find available hosts
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip), timeout=timeout, iface=interface, verbose=False)

    # Extract host information from response packets
    hosts = []
    for snd, rcv in ans:
        mac_address = rcv[Ether].src
        ip_address = rcv[ARP].psrc
        vendor = ""
        try:
            vendor = get_vendor(mac_address)
        except:
            pass
        hosts.append({'mac_address': mac_address, 'ip_address': ip_address, 'vendor': vendor})

    return hosts


def get_vendor(mac_address):
    """
    Gets the vendor name for a given MAC address using the MAC address lookup API.

    :param mac_address: The MAC address to lookup.
    :return: The vendor name, or an empty string if not found.
    """

    url = f"https://macvendors.com/query/{mac_address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', {}).get('company', '')
    return ""


def print_hosts(hosts):
    """
    Prints information about the available hosts to the console.

    :param hosts: A list of dictionaries containing host information.
    """

    print(f"{'IP Address':<20} {'MAC Address':<20} {'Vendor':<20}")
    for host in hosts:
        print(f"{host['ip_address']:<20} {host['mac_address']:<20} {host['vendor']:<20}")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Wireless Network Analyzer')
    parser.add_argument('-i', '--interface', type=str, help='The network interface to use', required=True)
    parser.add_argument('-t', '--target', type=str, help='The target IP address or range', default=None)
    parser.add_argument('-o', '--output', type=str, help='The output file', default=None)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output', default=False)
    args = parser.parse_args()

    # Scan the network
    hosts = scan_network(args.interface, args.target)

    # Print the available hosts
   
