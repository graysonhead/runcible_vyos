from runcible.drivers.driver import DriverBase
from runcible_vyos.providers.system import VyosSystemProvider
from runcible_vyos.providers.interfaces import VyosInterfacesProvider
from runcible_vyos.protocols.ssh import VyosInteractiveSSH


class VyosDriver(DriverBase):
    """
    The driver is what associates providers to modules and assigns protocol classes.

    Additionally, the Driver can have the following methods that allow you to take preparation
    or cleanup steps:
    pre_plan_tasks
    post_plan_tasks
    pre_exec_tasks
    post_exec_tasks

    Each of these methods are passed the device instance when run, allowing you to
    use its methods to send commands or store key/value pairs
    """
    # The driver name is the key that a user would use to select the driver
    driver_name = "vyos"

    # The provider map associates providers to modules
    module_provider_map = {
        "system": VyosSystemProvider,
        "interfaces": VyosInterfacesProvider
    }
    # The protocol map maps protocols to identifier strings
    protocol_map = {
        "ssh": VyosInteractiveSSH
    }

    # This method gets run before the device.plan() method is called
    @staticmethod
    def pre_plan_tasks(device):
        # This puts the device terminal into a configure mode
        device.send_command('configure')

    # This method gets run after device.exec() completes its task, but before callbacks are rendered
    @staticmethod
    def post_exec_tasks(device):
        # These commands commit the changes, save them, and then close the configure terminal
        device.send_command('commit')
        device.send_command('save')
        device.send_command('exit')
