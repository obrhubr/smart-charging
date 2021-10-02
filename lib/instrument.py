import minimalmodbus

def create_instrument(usb):
    instrument = minimalmodbus.Instrument(usb, 1)
    instrument.serial.baudrate = 57600
    return instrument