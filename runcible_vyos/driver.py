from runcible.drivers.driver import DriverBase
from runcible_vyos.providers.system import VyosSystemProvider

class VyosDriver(DriverBase):
    driver_name = "vyos"

    module_provider_map = {
        "system": VyosSystemProvider
    }

    @staticmethod
    def pre_exec_tasks(device):
        device.send_command('configure')

    @staticmethod
    def post_exec_tasks(device):
        device.send_command('commit')
        device.send_command('save')
        device.send_command('exit')
