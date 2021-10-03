__author__ = "Nuno Moura"
__copyright__ = "Copyright 2021, FiberGateway_MEO_MODEL_GR241AG"
__license__ = "MIT"
__version__ = "1"
__maintainer__ = "Nuno Moura"
__email__ = "a21250606@alunos.isec.pt"
__status__ = "Prototype"
__description__ = "Tool to Parse some data from  network device FiberGateway MEO Model(GR241AG) "
import os
import argparse
import json
import sys
import pexpect
from AlticeFiberGateway import FiberGatewayMEO
from Utilities import *
from Config import Config

# MODEL: GR241AG
# FiberGateway MEO (GR241AG)


if __name__ == '__main__':
    try:

        #username, passwd = get_credentials()
        #hostname = get_ip_from_remote_meo_host()
        username = Config.USERNAME
        passwd = Config.PASSWORD
        hostname = Config.HOSTNAME
        # create a telnet session with device
        session1 = FiberGatewayMEO(hostname, username, passwd)
        session1.connect()

        # # DUMP TO FILES
        # result =  session1.dump_device_configurations_to_file()
        # print(result)

        # # # INTERFACES
        # interfaces_status = session1.get_lan_interfaces()
        # print(json.dumps(interfaces_status, indent=4))
        #
        # # # # ARP
        # arp_table = session1.get_arp_table()
        # print(json.dumps(arp_table, indent=4))


        # # # IPV4 and IPV6 DHCP leases
        # #  # /cli/lan/dhcp/show
        #dhcp_leases = session1.get_ipv4_dhcp_leases()
        #print(json.dumps(dhcp_leases, indent=4))
        #
        #
        # # /cli/lan/dhcp/show-ipv6
        # dhcpIPV6_leases = session1.get_IPV6_dhcp_leases()
        # print(json.dumps(dhcpIPV6_leases, indent=4))

        # # # /debug/show-diagnostics
        # network_diagnostics = session1.get_diagnostics()
        # print(json.dumps(network_diagnostics, indent=4))

        # # DEVICE INFO
        device_info_data = session1.get_device_info()
        print(json.dumps(device_info_data, indent=4))

        # DISCONNECT FROM DEVICE
        # TODO
        #  verify close() or quit
        session1.disconnect()

    except KeyboardInterrupt as error:
        session1.disconnect()
        print(green("SEE YOU"))
        sys.exit("See you later! Bye!")
    #except pexpect.exceptions.EOF as error:
    except pexpect.ExceptionPexpect as error:
        print("----")
        sys.exit(f"See you later!\nBye!\n \tPexpect error:\n {error}")




