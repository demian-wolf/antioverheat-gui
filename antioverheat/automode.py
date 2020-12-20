import threading
import time

import core


class AutomodeThread(threading.Thread):
    def __init__(self, sudo_password):
        super().__init__()
        
        self.daemon = True

        self.enabled = True
        self.sudo_password = sudo_password

    def run(self):
        while self.enabled:
            self.adjust_temperature()
            time.sleep(5)
    
    def stop(self):
        self.enabled = False

    def adjust_temperature(self):
        _, temperature = min(core.get_cpu_cores(), key=lambda core_info: core_info[1])
        current_max_fpolicy = core.get_current_fpolicy()[-1]
        if current_max_fpolicy == core.get_hardware_limits():
            return
        if temperature > 90:
            core.set_max_fpolicy(self.sudo_password, core.get_hardware_limits()[0])
            return
        if temperature > 70:
            core.set_max_fpolicy(self.sudo_password, current_max_fpolicy - 100)
            return
        core.set_max_fpolicy(self.sudo_password, current_max_fpolicy + 100)

if __name__ == "__main__":
    AutomodeThread().start()
