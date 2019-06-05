
from ydk.services import CodecService, NetconfService, Datastore
from ydk.providers import CodecServiceProvider, NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg as ifmgr_model
import exerciseutil

def prepare_config(datafile):
    data = ''
    # read xml file passes
    with open(datafile) as fh:
        data = fh.read()
    
    #associate this with codec service to get an ydk object
    codec = CodecService()
    return codec.decode(CodecServiceProvider(type='xml'), data)

def run(args):
    ''' This function uses PET Stack (via YDK) 
        and configures the device 
    '''

    # setup the protocol and transport
    # Use YDK provided NetconfService and NetconfServiceProvider
    ncapi = NetconfService()
    ncsession = NetconfServiceProvider(address="198.18.1.11",
                                      port=830,
                                      username="admin",
                                      password="admin",
                                      protocol="ssh")

    # setup the encoded content
    data = prepare_config(args.xml)
   
    # Perform operation - send to the device
    rsp = ncapi.edit_config(ncsession, Datastore.candidate, data)

    # commit the content
    ncapi.commit(ncsession)

if __name__ == '__main__':
    args = exerciseutil.parse_arguments()
    run(args)
