import bluetooth
import subprocess

class BluetoothScanner:

    def __init__(self):
        self.devices = []

    def scan_devices(self):
        self.devices = []
        nearby_devices = bluetooth.discover_devices()
        for bdaddr in nearby_devices:
            device = {}
            device['mac_address'] = bdaddr
            device['name'] = bluetooth.lookup_name(bdaddr)
            device['services'] = self.get_device_services(bdaddr)
            device['vendor'] = self.get_device_vendor(bdaddr)
            self.devices.append(device)

    def get_device_services(self, mac_address):
        services = []
        try:
            services = bluetooth.find_service(address=mac_address)
        except:
            pass
        return services

    def get_device_vendor(self, mac_address):
        vendor = ""
        try:
            output = subprocess.check_output(['arp', '-a', mac_address])
            lines = output.decode().split('\n')
            for line in lines:
                if mac_address in line:
                    vendor = line.split()[1]
        except:
            pass
        return vendor

    def print_devices(self):
        for device in self.devices:
            print(f"Device Name: {device['name']}")
            print(f"MAC Address: {device['mac_address']}")
            print(f"Vendor: {device['vendor']}")
            if device['services']:
                print("Services:")
                for service in device['services']:
                    print(f"\t{service['name']} ({service['protocol']})")
            print()

    def pen_test_device(self, mac_address):
        services = self.get_device_services(mac_address)
        vendor = self.get_device_vendor(mac_address)
        print(f"Pen testing {mac_address} ({vendor}):")
        for service in services:
            print(f"\tTesting service {service['name']} ({service['protocol']})")
            # perform pen testing on service

