import minimalmodbus

def create_instrument():
    # Find usb port by checking the list of files in "/dev" and searching for USB devices
    r = re.compile("ttyUSB")
    usb = list(filter(r.match, os.listdir("/dev")))[0]

    print("USB DEVICE USED: ", usb)

    instrument = minimalmodbus.Instrument(usb, 1)
    instrument.serial.baudrate = 57600
    return instrument