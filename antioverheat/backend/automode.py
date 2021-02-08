import threading
import time

from .api import CPUPowerAPI

class AutomodeThread(threading.Thread):
    def __init__(self, sudo_password, enabled=False):
        super().__init__()

        self.api = CPUPowerAPI()

        self.daemon = True

        self.sudo_password = sudo_password
        self.enabled = enabled

    def run(self):
        while True:
            if not self.enabled:
                continue
            self.adjust_temperature()
            time.sleep(5)

    def start(self):
        self.enabled = True

    def stop(self):
        self.enabled = False

    def toggle(self):
        self.enabled = bool(bool(self.enabled) ^ 1)

    def adjust_temperature(self):
        _, temperature = min(CPUPowerAPI().get_cpu_cores(), key=lambda core_info: core_info[1])
        current_max_fpolicy = self.api.get_current_fpolicy()[-1]
        if current_max_fpolicy == self.api.hardware_limits:
            return
        if temperature > 90:
            self.api.set_max_fpolicy(self.api.hardware_limits[0])
            return
        if temperature > 70:
            self.api.set_max_fpolicy(current_max_fpolicy - 100)
            return
        if temperature < 65:
            self.api.set_max_fpolicy(current_max_fpolicy + 100)
