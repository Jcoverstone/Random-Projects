from scapy.all import *

def analyze_wifi():
    # Set interface to monitor mode
    os.system("ifconfig wlan0 down")
    os.system("iwconfig wlan0 mode monitor")
    os.system("ifconfig wlan0 up")

    # Scan for wireless networks
    packets = sniff(iface="wlan0", count=10, prn=lambda x:x.sprintf("{Dot11Beacon:%Dot11.addr3%\n%Dot11Beacon.info%\n%PrismHeader.channel%\n%Dot11Beacon.cap%}"))

    # Display network information
    for packet in packets:
        print("SSID: " + packet.info.decode("utf-8"))
        print("BSSID: " + packet.addr3)
        print("Channel: " + str(int(ord(packet[PrismHeader].channel))))
        print("Encryption: " + ("Open" if packet.cap == 0x1104 else "WEP" if packet.cap & 0x0040 else "WPA/WPA2"))
        print("Associated devices: " + str(packet.addr3))