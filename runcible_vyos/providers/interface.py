from runcible.modules.interface import Interface, InterfaceResources
from runcible.core.need import NeedOperation as Op


class VyosInterfaceProvider:
    supported_attributes = [
        InterfaceResources.VLANS
    ]