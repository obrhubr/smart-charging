import minimalmodbus

def create_instrument(usb):
    instrument = minimalmodbus.Instrument(usb, 1)
    return instrument