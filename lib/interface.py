import minimalmodbus

# Read temperature from charger
def read_temperature(instrument):
    try:
        return instrument.read_register(303, 0)
    except IOError as e:
        raise IOError('Failed to write to instrument: ' + str(e)) from e

# Write if charging is allowed
def write_charging_allowed(instrument, value):
    try:
        return instrument.write_register(100, value, 0)
    except IOError as e:
        raise IOError('Failed to write to instrument') from e

# Read if charging is allowed
def read_charging_allowed(instrument):
    try:
        return instrument.read_register(100, 0)
    except IOError as e:
        raise IOError('Failed to write to instrument') from e

# Write at how many amps the car will be charged
def write_charging_amps(instrument, value):
    try:
        return instrument.write_register(101, value, 0)
    except IOError as e:
        raise IOError('Failed to write to instrument') from e

# Read at how many amps the car will be charged
def read_charging_amps(instrument):
    try:
        return instrument.read_register(101, 0)
    except IOError as e:
        raise IOError('Failed to write to instrument') from e