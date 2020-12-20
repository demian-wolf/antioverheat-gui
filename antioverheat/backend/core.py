import subprocess
import os
import re

import sensors


class UnknownFrequencyUnitError(Exception):
    pass

def to_mhz_value(string):
    """Converts the given frequency to MHz.

    :param string: string like "1.5 GHz"
    :type string: string

    :returns: the CPU frequency value in MHz
    :rtype: float

    :example:
    >>> self.to_mhz_value("1 GHz")
    1000.0
    >>> self.to_mhz_value("900 MHz")
    900.0
    >>> self.to_mhz_value("3.2 GHz")
    3200.0
    >>> self.to_mhz_value("3.2 hahaha")
    UnknownFrequencyUnitError: hahaha
    """
    
    UNITS = {"GHz": 1000, "MHz": 1}
    value, unit = string.split()
    value = float(value)
    coeff = UNITS.get(unit)
    if coeff:
        return value * coeff
    raise UnknownFrequencyUnitError(unit)

# TODO: rewrite these ugly functions using regexes

def get_hardware_limits():
    """Gets and returns hardware limits in MHz."""
    shell_output = subprocess.check_output("cpupower frequency-info | grep \"hardware limits\"", shell=True)
    shell_output = shell_output.decode().strip()
    return tuple(map(to_mhz_value, shell_output.split(": ")[-1].split(" - ")))

def get_current_fpolicy():
    """Gets and returns current cpu frequency policy in MHz."""
    shell_output = subprocess.check_output("cpupower frequency-info | grep \"should be within\"", shell=True)
    shell_output = shell_output.decode().strip()[:-1].split()
    return tuple(map(to_mhz_value, (" ".join(shell_output[-5:-3]), " ".join(shell_output[-2:]))))


def set_max_fpolicy(pwd, mhz_fr):
    os.system("echo {} | sudo -S cpupower frequency-set -u {}MHz"\
                  .format(pwd, mhz_fr))

def get_cpu_cores():
    sensors.init()
    for chip in sensors.iter_detected_chips():
        for feature in chip:
            if "Core" in feature.label:
                yield (feature.label, feature.get_value())
    sensors.cleanup()
