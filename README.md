### Project Name: 
    FiberGateway MEO ALTICE MODEL_GR241AG Parser
### Description: 
    Extract and Parse semi-structured data from FiberGateway MEO ALTICE MODEL_GR241AG.
    
### Version:
    1
### Requirements: 
    OS: linux.
    For Python3: requirements.txt
### Motivation
    Training scripting with Python
    Ingest the json data extracted from the device in an ELK Stack deployed into a Linux OS, 
    with Podman containers.

___
### How to use it, from a python script:
___


### Example 1: print out arp table
```
# FILE: main.py

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
        username = Config.USERNAME
        passwd = Config.PASSWORD
        hostname = Config.HOSTNAME
        # create a telnet session with device 
        session1 = FiberGatewayMEO(hostname, username, passwd)
        session1.connect()

        # # # ARP TABLE
        arp_table = session1.get_arp_table()
        print(json.dumps(arp_table, indent=4))


        # DISCONNECT FROM DEVICE
        session1.disconnect()

    except KeyboardInterrupt as error:
        session1.disconnect()
        print(green("SEE YOU"))
        sys.exit("See you later! Bye!")
    #except pexpect.exceptions.EOF as error:
    except pexpect.ExceptionPexpect as error:
        print("----")
        sys.exit(f"See you later!\nBye!\n \tPexpect error:\n {error}")

```


### 

### Example 2: Dump device configuration fo files
  
 ```
# File: main.py

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

        # DUMP TO FILES
        result =  session1.dump_device_configurations_to_file()
        print(result)

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


 ``` 


### 

### Example 3: Interfaces
  
 ```
# File: main.py

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

        # # # INTERFACES
        interfaces_status = session1.get_lan_interfaces()
        print(json.dumps(interfaces_status, indent=4))

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


 ``` 


## 

### Example 4: DHCP4 and DHCP6 Leases
  
 ```
# File: main.py

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


        # # # IPV4 and IPV6 DHCP leases
        # # IPV4
        # #  # /cli/lan/dhcp/show
        dhcp_leases = session1.get_ipv4_dhcp_leases()
        print(json.dumps(dhcp_leases, indent=4))
        #
        # # IPV6
        # /cli/lan/dhcp/show-ipv6
        dhcpIPV6_leases = session1.get_IPV6_dhcp_leases()
        print(json.dumps(dhcpIPV46_leases, indent=4))

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


 ``` 


## 

### Example 5: Connection status of your local network: LAN and Wifi
  
 ```
# File: main.py

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

        # # # /debug/show-diagnostics
        network_diagnostics = session1.get_diagnostics()
        print(json.dumps(network_diagnostics, indent=4))

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


 ``` 



## 

### Example 6: Device Information
  
 ```
# File: main.py

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


 ``` 

### MEO ALTICE GATEWAY CLI:
   __(Reference) Available Commands via Telnet connection from command line:__
   
   ``   Example: telnet 192.168.1.254 
   ``

      + cli[@cd, @clear, @dir, @help, @mem, @quit, @tree]
       + arp[@clear-arps, @show]
       + debug[@nslookup, @ping, @reboot-cause, @show-diagnostics, @traceroute]
       + device-info[@show]
       + lan[@config, @show]
          + bridge-mode[@config, @show]
          + dhcp[@clear-leases, @show, @show-ipv6]
          + interfaces[@config, @show]
          + ipv6[@show]
          + static-lease[@create, @remove, @show]
          + stp[@config, @show]
       + management[@reboot, @restore-default, @restore-partial]
          + access-control[@change-pw]
             + users[@create, @remove, @show]
          + ntp[@config, @show]
          + storage[@create, @remove, @show]
       + nat[]
          + dmz-host[@disable, @enable, @show]
          + nat1:1[@config, @create, @remove, @show]
          + port-triggering[@create, @remove, @show]
          + virtual-servers[@create, @remove, @show]
       + parental-control[]
          + time-restriction[@create, @remove, @show]
          + url-filter[@create, @list-type, @remove, @show]
       + routing[]
          + static-route[@show]
       + statistics[]
          + lan[@reset, @show]
          + optical[@reset, @show]
          + wan[@reset, @show]
       + upnp[@config, @show]
       + voice[@show, @show-fxs]
       + wan[@show]
          + bridge[@show]
          + gre[@show]
          + ipoe[@show]
          + wantype[@show]
       + wireless[@show-defaults, @show-neighborhood, @show-stationinfo, @show-stationinfo-counters]
          + basic[@config, @show]
          + mac-filtering[@add, @config, @remove, @show]
          + scan[@show-channel-stats, @trigger-autochannel]
          + security[@config, @show]
          + wps[@show_status, @trigger_pbc]
