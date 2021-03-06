import minimalmodbus
import re
import os

def create_instrument():
    # Find usb port by checking the list of files in "/dev" and searching for USB devices
    r = re.compile("ttyUSB")
    usb = list(filter(r.match, os.listdir("/dev")))[0]

    print("USB DEVICE USED: " + str(usb), flush=True)

    instrument = minimalmodbus.Instrument("/dev/" + usb, 1)
    instrument.serial.baudrate = 57600
    return instrument