from runcible.providers.provider_array import ProviderArrayBase
from runcible.modules.interfaces import Interfaces
from runcible_vyos.providers.interface import VyosInterfaceProvider


class VyosInterfacesProvider(ProviderArrayBase):
    provides_for = Interfaces
    sub_module_provider = VyosInterfaceProvider

    def get_cstate(self):
        interfaces = []
        interface_list_raw_lines = self.device.send_command('show interfaces ethernet')
        for line in interface_list_raw_lines:
            if line.strip().startswith('ethernet'):
                line_components = line.strip().split(' ')
                interfaces.append(line_components[1])


