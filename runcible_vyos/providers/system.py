from runcible.modules.system import System, SystemResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op

# Map the values returned by the vyos parser to their respective values in the runcible interface
attribute_map = {
    "host-name": SystemResources.HOSTNAME
}


class VyosSystemProvider(ProviderBase):
    """
    The only two methods that a provider needs to provide are get_cstate (which fetches the current state of the
    module's attributes on the target device. And the fix_needs method, which takes the need objects provided by the
    parent class and fixes them.
    """
    # We must specify the module that this provider provides for
    provides_for = System
    # We also need to specify which attributes this module implements. If a user calls an un-implemented attribute
    # They will receive a warning.
    supported_attributes = [
        SystemResources.HOSTNAME
    ]

    def get_cstate(self):
        """
        Gets the current state of all attributes in the module on the target device.
        :return:
        """
        config_dict = {}
        config = self.device.retrieve('configuration')
        system_dict = config.get('system', {})
        for key, value in system_dict.items():
            if key in attribute_map:
                config_dict.update({attribute_map[key]: value})
        return System(config_dict)

    def fix_needs(self):
        """
        This method receives an array of need objects and iterates through them, taking the action
        needed to resolve each need.

        If any needs are left uncompleted, an exception will be raised
        :return:
        """
        for need in self.needed_actions:
            if need.attribute is SystemResources.HOSTNAME:
                if need.operation is Op.SET:
                    # Set the hostname to the value specified by the need
                    self._set_hostname(need.value)
                    # Mark the task as complete
                    self.complete(need)

    def _set_hostname(self, hostname):
        return self.device.send_command(f"set system host-name {hostname}")

    def _get_hostname(self):
        lines = self.device.send_command("show system host-name")
        try:
            hostname = lines[1].strip().split(' ')[1]
        except IndexError:
            return ''
        return hostname
