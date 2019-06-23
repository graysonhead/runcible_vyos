from runcible.drivers.driver import DriverBase
from runcible_vyos.providers.system import VyosSystemProvider
from runcible_vyos.protocols.ssh import VyosInteractiveSSH


class VyosDriver(DriverBase):
    driver_name = "vyos"

    module_provider_map = {
        "system": VyosSystemProvider
    }
    protocol_map = {
        "ssh": VyosInteractiveSSH
    }

    @staticmethod
    def pre_plan_tasks(device):
        device.send_command('configure')

    @staticmethod
    def post_exec_tasks(device):
        device.send_command('commit')
        device.send_command('save')
        device.send_command('exit')
