import subprocess
import os

import sensors

from .exceptions import UnknownFrequencyUnitError, SudoPasswordRequired


class CPUCore(object):
    def __init__(self, name, value):
        self.name, self.value = name, value

class CPUPowerAPI(object):
    """API for cpupower."""

    # TODO: rewrite these ugly methods using JSON output and regexes

    def __init__(self, sudo_password=None):
        self.sudo_password = sudo_password

        self.__setup_hardware_limits()

    @staticmethod
    def to_mhz_value(string):
        """Converts the given frequency to MHz.

        :param string: string like "1.5 GHz"
        :type string: string

        :returns: the CPU frequency value in MHz
        :rtype: float

        :example:
        >>> CPUPowerAPI.to_mhz_value("1 GHz")
        1000.0
        >>> CPUPowerAPI.to_mhz_value("900 MHz")
        900.0
        >>> CPUPowerAPI.to_mhz_value("3.2 GHz")
        3200.0
        >>> CPUPowerAPI.to_mhz_value("3.2 hahaha")
        UnknownFrequencyUnitError: hahaha
        """

        UNITS = {"GHz": 1000, "MHz": 1}
        value, unit = string.split()
        value = float(value)
        coeff = UNITS.get(unit)
        if coeff:
            return value * coeff
        raise UnknownFrequencyUnitError(unit)

    def __setup_hardware_limits(self):
        shell_output = subprocess.check_output("cpupower frequency-info | grep \"hardware limits\"", shell=True)
        shell_output = shell_output.decode().strip()
        self.__hardware_limits = tuple(map(self.to_mhz_value, shell_output.split(": ")[-1].split(" - ")))

    @property
    def hardware_limits(self):
        return self.__hardware_limits

    def get_current_fpolicy(self):
        """Gets current cpu frequency policy in MHz."""
        shell_output = subprocess.check_output("cpupower frequency-info | grep \"should be within\"", shell=True)
        shell_output = shell_output.decode().strip()[:-1].split()
        return tuple(map(self.to_mhz_value, (" ".join(shell_output[-5:-3]), " ".join(shell_output[-2:]))))

    def set_max_fpolicy(self, mhz_fr):
        """Sets maximum frequency policy.

        Raises: SudoPasswordRequired if the password was not passed to the constructor."""
        if self.sudo_password is None:
            raise SudoPasswordRequired
        os.system("echo {} | sudo -S cpupower frequency-set -u {}MHz".format(self.sudo_password, mhz_fr))

    def get_cpu_cores(self):
        """Gets names of CPU cores and their temperature values."""
        sensors.init()
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                if "Core" in feature.label:
                    yield CPUCore(feature.label, feature.get_value())
        sensors.cleanup()
