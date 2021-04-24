import subprocess

import sensors

from .exceptions import UnknownFrequencyUnitError


class CPUCore(object):
    def __init__(self, name, value):
        self.name, self.value = name, value

class CPUPowerAPI(object):
    """API for cpupower."""

    # TODO: rewrite the ugly methods below to use JSON output and/or regexes

    def __init__(self):
        shell_output = subprocess.check_output("cpupower frequency-info | grep \"hardware limits\"", shell=True)
        shell_output = shell_output.decode().strip()
        self.__hardware_limits = tuple(map(self.to_mhz_value, shell_output.split(": ")[-1].split(" - ")))

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
        if unit in UNITS:
            return value * UNITS[unit]
        raise UnknownFrequencyUnitError(unit)

    @property
    def hardware_limits(self):
        return self.__hardware_limits

    def get_policy(self):
        """Gets current CPU frequency policy in MHz."""
        shell_output = subprocess.check_output("cpupower frequency-info | grep \"should be within\"", shell=True)
        shell_output = shell_output.decode().strip()[:-1].split()
        return tuple(map(self.to_mhz_value, (" ".join(shell_output[-5:-3]), " ".join(shell_output[-2:]))))

    def set_policy(self, **kwargs):
        """Sets frequency policy.

        Raises: SudoPasswordRequired if the password was not passed to the constructor."""
        if not kwargs:
            raise ValueError("you must specify some kwargs")

        # FIXME: min must be after max in case both are given
        for arg, value in kwargs.items():
            if value is not None:
                arg = "-" + arg if len(arg) == 1 else "--" + arg
                subprocess.call("cpupower frequency-set {} {}MHz"\
                                .format(arg, value),
                                shell=True)

    def get_cpu_cores(self):
        """Gets names of CPU cores and their temperature values."""
        sensors.init()
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                if "Core" in feature.label:
                    yield CPUCore(feature.label, feature.get_value())
        sensors.cleanup()
