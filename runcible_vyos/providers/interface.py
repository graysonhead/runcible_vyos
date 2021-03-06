from runcible.modules.interface import Interface, InterfaceResources
from runcible.providers.sub_provider import SubProviderBase
from runcible.core.need import NeedOperation as Op


# Map the values returned by the vyos parser to their respective values in the runcible interface
attribute_map = {
            "address": InterfaceResources.IPV4_ADDRESS,
            "mtu": InterfaceResources.MTU
        }


class VyosInterfaceProvider(SubProviderBase):
    supported_attributes = [
        InterfaceResources.MTU,
        InterfaceResources.IPV4_ADDRESS
    ]

    def get_cstate(self, interface: str):
        config = self.device.retrieve('configuration')
        config_dict = {"name": interface}
        if config.get("interfaces", None):
            for key, value in config['interfaces'].items():
                if config["interfaces"][key].get(interface, None):
                    for key, attrvalue in value[interface].items():
                        if key in attribute_map:
                            config_dict.update({attribute_map[key]: attrvalue})
        return Interface(config_dict)

    def _get_mtu(self, interface):
        result = self.device.send_command(f"show interfaces ethernet {interface} mtu")
        if result[1] == 'Configuration under specified path is empty':
            return 1500
        else:
            return int(result[1].strip('mtu '))

    def _get_ipv4_address(self, interface):
        result = self.device.send_command(f"show interfaces ethernet {interface} address")
        if result[1] == 'Configuration under specified path is empty':
            return None
        else:
            return result[1].strip('address ')

    def _set_ipv4_address(self, interface, address):
        self.device.send_command(f"delete interface ethernet {interface} address")
        return self.device.send_command(f"set interfaces ethernet {interface} address {address}")

    def _clear_ipv4_address(self, interface):
        return self.device.send_command(f"delete interface ethernet {interface} address")

    def _set_mtu(self, interface, mtu):
        result = self.device.send_command(f"set interfaces ethernet {interface} mtu {mtu}")
        return result

    def fix_need(self, need):
        if need.attribute == InterfaceResources.MTU:
            if need.operation == Op.SET:
                self._set_mtu(need.module, need.value)
                self.complete(need)
        if need.attribute == InterfaceResources.IPV4_ADDRESS:
            if need.operation == Op.SET:
                self._set_ipv4_address(need.module, need.value)
                self.complete(need)
            if need.operation == Op.CLEAR:
                self._clear_ipv4_address(need.module)
                self.complete(need)