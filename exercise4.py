
from ydk.services import CodecService, NetconfService, Datastore
from ydk.providers import CodecServiceProvider, NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg as ifmgr_model
from ydk import types as ytypes
import exerciseutil

def prepare_config():
    ''' use YDK object and populate the data
        engine takes care of XML encoding
    '''

    interface_configurations = ifmgr_model.InterfaceConfigurations()
    interface = interface_configurations.InterfaceConfiguration()
    interface_configurations.interface_configuration.append(interface)

    interface.active = "act"
    interface.interface_name = "Loopback0"
    interface.description = "Demo interface config via YDK ifmgr_model"
    interface.interface_virtual = ytypes.Empty()
    primary = interface.ipv4_network.addresses.Primary()
    interface.ipv4_network.addresses.primary = primary
    primary.address = "172.16.255.1"
    primary.netmask = "255.255.255.255"
    return interface_configurations 

def run(args):
    ''' This function uses PET Stack (via YDK) 
        and configures the device 
    '''

    # setup the protocol and transport
    ncapi = NetconfService()
    ncsession = NetconfServiceProvider(address="198.18.1.11",
                                      port=830,
                                      username="admin",
                                      password="admin",
                                      protocol="ssh")

    # setup the encoded content
    data = prepare_config()
   
    # Perform an action - send to the device
    rsp = ncapi.edit_config(ncsession, Datastore.candidate, data)

    # Perform an action - commit the content
    ncapi.commit(ncsession)

if __name__ == '__main__':
    args = exerciseutil.parse_arguments()
    run(args)
