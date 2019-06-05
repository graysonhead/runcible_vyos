from runcible.modules.system import System, SystemResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op


class VyosSystemProvider(ProviderBase):
    provides_for = System
    supported_attributes = [
        'hostname'
    ]

    def get_cstate(self):
        hostname = self._get_hostname('hostname').strip()
        return System({'hostname': hostname})

    def fix_needs(self):
        for need in self.needed_actions:
            if need.attribute is SystemResources.HOSTNAME:
                if need.operation is Op.SET:
                    self._set_hostname(need.value)
                    self.completed(need)

    def _set_hostname(self, hostname):
        return self.device.send_command(f"set system host-name {hostname}")

    def _get_hostname(self):
        return self.device.send_command("hostname")
