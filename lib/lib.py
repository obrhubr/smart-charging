import math

def convert_amps_to_kw(amps):
    power_factor = 0.8
    kw = (math.sqrt(3) * power_factor * amps * 380) / 1000

    return kw

def convert_kw_to_amps(kw):
    power_factor = 0.8
    amps = (1000 * kw) / (math.sqrt(3) * power_factor * 380)

    return amps