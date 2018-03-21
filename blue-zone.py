import bluetooth
import json
import sys
from datetime import datetime

class Device(object):
    def __init__(self, addr, name):
        self.addr = addr
        self.name = name
        self.present = False

    def __eq__(self, other):
        if isinstance(other, Device):
            return self.addr == other.addr
        else:
            return self.addr == other

    def scan(self):
        if bluetooth.lookup_name(self.addr):
            if not self.present:
                self.present = True
                print("%s + \"%s\" has entered the area" % (timestamp(), self.name))
        else:
            if self.present:
                if not (bluetooth.lookup_name(self.addr) or bluetooth.lookup_name(self.addr)):
                    self.present = False
                    print("%s - \"%s\" has left the area" % (timestamp(), self.name))

class Zone(object):
    def __init__(self, devices_file):
        self.devices_file = devices_file
        self.read_devices()

    def discover_devices(self):
        while True:
            new_devices = bluetooth.discover_devices(lookup_names=True)
            for addr, name in new_devices:
                if addr not in self.devices:
                    print("%s + Discovered new device %s labled \"%s\"" % (timestamp(), addr, name))
                    self.devices.append(Device(addr, name))
            self.save_devices()

    def scan_devices(self):
        while True:
            for device in self.devices:
                device.scan()

    def save_devices(self):
        json_devices = {}
        for device in self.devices:
            json_devices.update({
                device.addr: {"name": device.name}
            })
        with open(self.devices_file, 'w') as file:
            json.dump(json_devices, file, indent=2)

    def read_devices(self):
        self.devices = []
        try:
            with open(self.devices_file) as file:
                json_devices = json.load(file)
            for mac in json_devices:
                name = json_devices[mac]["name"]
                self.devices.append(Device(mac, name))
        except FileNotFoundError:
            pass

def timestamp():
    return str(datetime.now().replace(microsecond=0))

def main():
    zone = Zone("devices.json")
    if sys.argv[1] == "discover":
        zone.discover_devices()
    elif sys.argv[1] == "scan":
        zone.scan_devices()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass