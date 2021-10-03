
import sys
try:
    from Utilities import *
except ImportError as error:
    sys.exit(f'\n\n\tWe couldn"t load Color.py.'
              f'\n\t Error {error}'
              f'\n\t ')
from ProjectUtilities import replace_chars_from_cmds
try:
    import pexpect
except ImportError as error:
    sys.exit(f'We couldn"t load pexpect.'
             f'\n\n\tError {error}'
             f'\n\n\t Check if pexpect is installed.')

global CONFIG  # DECLARE GLOBAL
CONFIG = True  # DEFINE IT, first time definition

try:
    from Config import Config
except ImportError as error:
    print(f'\n\n\tWARNING: Not loading Configurations from file: "Config.py"'
          f' \n\tError: {error}'
          f'\n\n\t We will Load Defaults Configuration')
    #global CONFIG  # declare the existing of global Variable
    CONFIG = False
    pass


class FiberGatewayMEO:
    """
    EXTRACT SEMI-STRUCTURED DATA FROM network DEVICE and Tries to Parse it
        # MODEL: GR241AG
        # FiberGateway MEO (GR241AG)

    # SOURCE: https://stackoverflow.com/questions/45646852/create-one-pexpect-session-only-for-all-objects-in-python
    """
    def __init__(self, hostname=None, username=None, passwd=None):
        """

        :param hostname:<str>
        :param username:<str>
        :param passwd:<str>
        """


        # POSSIBLE COMMAND TO RUN ON DEVICE: BELOW DICT DATA struture REPRESENTS:
        #    <hash key>: (<cmd to Execute on the Remote Device>, <Description>)
        self.__MEO_DEVICE_COMMANDS = {
            '01': ('/arp/show', 'Arp table'),
            '02': ('/debug/show-diagnostics', None),
            '03': ('/device-info/show', 'Device general information '),
            '04': ('/management/storage/show', 'Check if a disk is configured'),
            '05': ('/management/ntp/show', 'NTP configurations'),
            '06': ('/management/access-control/users/show', 'Users Administrator configured on device'),
            '07': ('/lan/show', 'General Lan configuration'),
            '08': ('/lan/bridge-mode/show', "Useful to Check if bridge is enable"),
            '09': ('/lan/dhcp/show', 'Dhcp Ipv4 Leases'),
            '10': ('/lan/dhcp/show-ipv6', 'Dhcp Ipv6 Leases'),
            '11': ('/lan/interfaces/show', 'Device interfaces name status etc ...'),
            '12': ('/lan/ipv6/show', 'I don"t know, jerry... You know'),
            '13': ('/lan/static-lease/show', None),
            '14': ('/lan/stp/show', "Spanning "),  # spanning
            '15': ('/nat/dmz-host/show', None),
            '16': ('/nat/nat1:1/show', None),
            '17': ('/nat/port-triggering/show', None),
            '18': ('/nat/virtual-servers/show', None),
            '19': ('/parental-control/time-restriction/show', None),
            '20': ('/parental-control/url-filter/show', None),
            '21': ('/routing/static-route/show', None),
            '22': ('/statistics/lan/show --option=all', None),
            '23': ('/statistics/optical/show --option=all', None),
            '24': ('/statistics/wan/show --option=all', None),
            '25': ('/upnp/show', None),
            '26': ('/voice/show-fxs', None),
            '27': ('/wan/show', None),
            '28': ('/wan/bridge/show', None),
            '29': ('/wan/gre/show', None),
            '30': ('/wan/ipoe/show', None),
            '31': ('/wan/wantype/show', None),
            '32': ('/wireless/show-defaults', None),  # Raw Passwd! OCCLUDE THIS# TODO : WARNING NOTE: DONT LOG!
            #      '/wireless/show-neighborhood --wifi-index=[Wifi- Interface Index <0|1>]',
            '33': ('/wireless/show-neighborhood --wifi-index=0', None),  # TAKES TO MUCH TIME TO RUN ~= 3 to 6 seconds.
            '34': ('/wireless/show-stationinfo --wifi-index=0', None),
            '35': ('/wireless/show-stationinfo-counters --wifi-index=0', None),  # MOSTRA Oos MACs  wireless da MEO STATION
            '36': ('/wireless/basic/show --wifi-index=0', None),
            '37': ('/wireless/mac-filtering/show --wifi-index=0', None),
            '38': ('/wireless/scan/show-channel-stats --wifi-index=0', None),  # Takes 1 to 2 seconds to run
            '39': ('/wireless/scan/show-channel-stats --wifi-index=0', None),  # Takes 1 to 2 seconds to run
            '40': ('/wireless/scan/trigger-autochannel --wifi-index=0', None),  # Takes 4 to 6 seconds to run
                                       # returns wireless channel configured
            '41': ('/wireless/security/show --wifi-index=0', None),  # wifi security configurations TODO: DONT LOG THIS
            '42': ('/wireless/wps/show_status', None)  # WPS BUTTON ... IDLE or....
        }

        if CONFIG:
            # CREDENTIALS AND REMOTE HOSTNAME TO CONNECT
            # GET them FROM Configuration file
            self.__USERNAME = Config.USERNAME
            self.__PASSWD = Config.PASSWORD
            self.__HOSTNAME = Config.HOSTNAME

        # Get them from Developer
        if username:
            self.__USERNAME = username
        if passwd:
            self.__PASSWD = passwd
        if hostname:
            self.__HOSTNAME = hostname

        if CONFIG:
            # PEXPECT LOGGING
            # pexpect's LOG Configuration
            self.Is_log_enable = Config.PEXPECT_LOG_ENABLED
            self.LOG_FILENAME = Config.PEXPECT_LOG_FILENAME
        else:
            self.Is_log_enable = True  # Configure defaults ... We couldn t load from Config.py
            self.LOG_FILENAME = 'Meo_device_pexpect.log'

        # START LOGGING if Configured
        if self.Is_log_enable:
            self.LOG_FSOUT = open(self.LOG_FILENAME, 'ab')

        self.Is_connected = False
        self.telnet = None

        # FOR DUMPING ALL DEVICE CONFIGURATIONS IN FILE TEXTS.... THIS IS THE LOCATION
        if CONFIG:
            self.__DIRNAME_DEVICE_DUMPS = Config.DIRNAME_DEVICE_DUMPS
        else:
            # Store on the Class Folder # TODO: change this after ...
            self.__DIRNAME_DEVICE_DUMPS = 'DeviceDumpDir'

        # test_color() # FOR CHOOSING COLOR print The OUTPUTS

    def connect(self):
        """
        Create a telnet connection to Remote Meo Device <pexpect.child>
        :return:
        """
        self.telnet = pexpect.spawn('telnet ' + self.__HOSTNAME)
        self.telnet.expect('Login: ')
        #
        self.telnet.sendline(self.__USERNAME)  # SEND CREDENTIALS ... username
        self.telnet.expect('Password: ')
        self.telnet.sendline(self.__PASSWD)
        #
        self.telnet.expect('/cli> ')

        # START LOGGING, just right Here because we dont want password and user login to be cached in log file
        if self.Is_log_enable:
            self.telnet.logfile = self.LOG_FSOUT

        # Todo: Comment this. Xd)
        print(self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n"),
              self.telnet.after.decode("UTF-8").replace("\r\n\n", "\n"))
        self.Is_connected = True

    def disconnect(self):
        print(green("Bye bye. Have a nice day!!!"))
        self.telnet.sendline("quit")  # FORCE Telnet connection to close
        self.telnet.close()  # pexpect terminate child
        self.telnet, self.Is_connected = None, False

    def check_connection(self):
        print(self.__HOSTNAME + ' is ' + str(self.Is_connected))
        return self.Is_connected

    def send_command(self, command):
        self.telnet.sendline(command)
        self.telnet.expect('/cli> ')
        return self.telnet.before + self.telnet.after

    def get_device_info(self):
        if self.Is_connected:
            self.send_command("/device-info/show")
            # print("OUTPUT - telnet.before:")  # Interessa o before
            # print(self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n"))
            data = self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n").split("\n")
            output = {"Command": data[0].replace('\r', ''),
                      "Title": data[2].replace('\r', '').replace('|', '').strip()}
            key_pairs_data = []

            for index, line in enumerate(data[6:-2]):
                # print(index, line)
                line = line.split('|')
                _kp = (line[1].strip(), line[2].strip())
                key_pairs_data.append(_kp)

            output["ParameterValues"] = tuple(key_pairs_data)
            # print(json.dumps(output, indent=4))
            data_dictionary = self.__to_dictionary_device_info(output)
            return data_dictionary

    def get_arp_table(self) -> dict:
        """
        Get the FiberGateway network device ARP TABLE .
        :return: <dict> arp table data

        An EXAMPLE:
        {
        "Command": "/arp/show",
        "Title": "ARP configurations",
        "Devices": {
            "Device0": {
                "IpAddress": "192.168.1.69",
                "Flags": "Complete",
                "HwAddress": "1d:57:64:1f:50:01",
                "Device?MEO": "br0"
            },
            "Device1": {
                "IpAddress": "192.168.1.70",
                "Flags": "Complete",
                "HwAddress": "10:44:17:d7:00:bc",
                "Device?MEO": "br0"
            },
            ...,
            ...,
            ...,
            ...,
        }
        """

        if self.Is_connected:
            self.send_command("/arp/show")
            # print("OUTPUT - telnet.before:")  # Interessa o before
            # print(self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n"))
            data = self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n").split("\n")

            output = {"Command": data[0].replace('\r', ''),
                      "Title": data[2].replace('\r', '').replace('|', '').strip()
                      }
            key_pairs_data = []

            for index, line in enumerate(data[6:-1]):
                #  print(index, line)
                if '+----------------+' not in line:
                    line = line.split('|')
                    #  print(line)
                    _kp1 = ("IpAddress", line[1].strip())
                    _kp2 = ("Flags", line[2].strip())
                    _kp3 = ("HwAddress", line[3].strip())
                    _kp4 = ("Device?MEO", line[4].strip())
                    key_pairs_data.append([_kp1, _kp2, _kp3, _kp4])

            output["ParameterValues"] = tuple(key_pairs_data)
            data_dictionary = self.__to_dictionary(output)
            return data_dictionary

    def config_clear_arp_table(self):
        """
            NOTE: DONT USE THIS method
            Clear the arp pool/table
            Command to execute on device:
                '/arp/clear-arps --group-name=Default'
                    # group name Default
        """
        # WHEN WE run this command we will lose access to network device, so will we exit
        # TODO
        #  Test 1
        #   - Check if it is necessary to reboot de device or disconnect from power AC
        #     - WARNING - DONT USE THIS!
        if self.Is_connected:
            self.send_command("arp/clear-arps --group-name=Default")

    def get_diagnostics(self):
        """
        ----    LAN AND WIRELESS STATUS ----
        We will parse the CLI output   from network device , for the CLI command : /debug/show-diagnostics

        :return:<dict>
        {'Command': <str> 'command that generated this output',
         'Tittle1': <str> 'data description .IN these case LAN',
         'ParameterValues1': <list>, each element correspond to cli line
        ' Tittle2: <str> 'data description IN these case Wireless LAN',
        ' ParameterValues2': <list> each element correspond to cli line
        }
        """

        if self.Is_connected:
            self.send_command("/debug/show-diagnostics")

            # print("OUTPUT - telent.before:")  # Interessa o before
            # print(self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n"))  # TO SEE THE OUTPUT
            data = self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n").split("\n")

            output = {"Command": data[0].replace('\r', ''),
                      "Title1": data[2].replace('\r', '').replace('|', '').strip()
                      }
            key_pairs_data = []

            # for index, line in enumerate(data):
            #    print(index, line)

            for index, line in enumerate(data[6:10]):
                if '+---------------' not in line:
                    line = line.split('|')
                    _kp1 = ("Interface", line[1].strip())
                    _kp2 = ("OperationalStatus", line[2].strip())
                    _kp3 = ("DuplexMode", line[3].strip())
                    _kp4 = ("Speed", line[4].strip())
                    key_pairs_data.append([_kp1, _kp2, _kp3, _kp4])
            output["ParameterValues1"] = tuple(key_pairs_data)

            key_pairs_data = []
            output['Title2'] = data[12].replace('\r', '').replace('|', '').strip()
            for index, line in enumerate(data[16:20]):
                if '+-' not in line:
                    line = line.split('|')
                    _kp1 = ("Interface", line[1].strip())
                    _kp2 = ("OperationalStatus", line[2].strip())
                    key_pairs_data.append([_kp1, _kp2])

            output["ParameterValues2"] = tuple(key_pairs_data)
            # print(output)
            # print(json.dumps(output, indent=4))
            data_dictionary = self.__to_dictionary_diagnostics(output)
            return data_dictionary

    def get_lan_interfaces(self):
        """
        ----    LAN interfaces names and status
        We will parse the CLI output   from network device , for the CLI command : /lan/interfaces/lan

        :return:<dict>
        {'Command': <str> 'command that generated this output',
         'Tittle': <str> 'data description. in these case: Local Area Network (LAN) Ethernet Config',
         'ParameterValues': <list>, each element correspond to cli line. key value pairs ,
         like interface name, status ...
        }
        """

        if self.Is_connected:
            self.send_command("/lan/interfaces/show")
            # print(self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n"))  # TO SEE THE OUTPUT
            data = self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n").split("\n")

            output = {"Command": data[0].replace('\r', ''),
                      "Title": data[2].replace('\r', '').replace('|', '').strip()
                      }
            key_pairs_data = []

            # for index, line in enumerate(data):

            for index, line in enumerate(data[6:10]):
                # print(index, line)
                if '+----------------+' not in line:
                    line = line.split('|')
                    # print(line)
                    _kp1 = ("Interface", line[1].strip())
                    _kp2 = ("AdminStatus", line[2].strip())
                    _kp3 = ("SpeedMbPerSecond", line[3].strip())
                    key_pairs_data.append([_kp1, _kp2, _kp3])

            output["ParameterValues"] = tuple(key_pairs_data)
            # print(output)
            data_dictionary = self.__to_dictionary(output)
            return data_dictionary

    def is_bridge_mode(self):
        """
         Bridge Mode on LAN4 interface <enable|disable>
         We are expecting to be enable or disabable
        :return:
        """

        if self.Is_connected:
            self.send_command("/lan/bridge-mode/show")
            # print(self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n"))  # TO SEE THE OUTPUT
            data = self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n").split("\n")

            # output = {"Command": data[0].replace('\r', ''),
            #          "Title": data[2].replace('\r', '').replace('|', '').strip(),
            #          "ParameterValues": ("Status", data[6].replace('\r', '').replace('|', '').strip())}

            if data[6].replace('\r', '').replace('|', '').strip() == "Enabled":
                return True, "bridge Mode on LAN4 interface"

            return False

    def get_ipv4_dhcp_leases(self):
        """
        We can get DHCP leases. .... hostname, ip, macaddress ....
        :return <dict>
        """

        if self.Is_connected:
            self.send_command("/lan/dhcp/show")
            # print(self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n"))  # TO SEE THE OUTPUT
            data = self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n").split("\n")

            output = {"Command": data[0].replace('\r', ''),
                      "Title": data[2].replace('\r', '').replace('|', '').strip()
                      }

            # for index, line in enumerate(data):
            #    print(index, line)

            key_pairs_data = []

            for index, line in enumerate(data[6:-1]):
                if '+-------' not in line:
                    line = line.split('|')
                    #print(line)
                    _kp1 = ("Hostname", line[1].strip())
                    _kp2 = ("MacAddress", line[2].strip())
                    _kp3 = ("IPV4Address", line[3].strip())
                    _kp4 = ("Expires in", line[4].strip())
                    _kp5 = ("Port", line[5].strip())
                    _kp6 = ("Active", line[6].strip())
                    _kp7 = ("Type", line[7].strip())
                    key_pairs_data.append([_kp1, _kp2, _kp3, _kp4, _kp5, _kp6, _kp7])

            output["ParameterValues"] = tuple(key_pairs_data)
            # print(json.dumps(output, indent=4))
            data_dictionary = self.__to_dictionary(output)
            return data_dictionary

    def get_IPV6_dhcp_leases(self):
        """
        ----    LAN interfaces names and status
        We will parse the CLI output   from network device , for the CLI command : /lan/interfaces/lan

        :return:<dict>
        {'Command': <str> 'command that generated this output',
         'Tittle': <str> 'data description. in these case: Local Area Network (LAN) Ethernet Config',
         'ParameterValues': <list>, each element correspond to cli line. key value pairs ,
         like interface name, status ...
        }
        """

        if self.Is_connected:
            self.send_command("/lan/dhcp/show-ipv6")
            # print(self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n"))  # TO SEE THE OUTPUT
            data = self.telnet.before.decode("UTF-8").replace("\r\n\n", "\n").split("\n")

            output = {"Command": data[0].replace('\r', ''),
                      "Title": data[2].replace('\r', '').replace('|', '').strip()
                      }

            key_pairs_data = []

            for index, line in enumerate(data[6:-1]):
                if '+----' not in line:
                    line = line.split('|')
                    # print(line)
                    _kp1 = ("Hostname", line[1].strip())
                    _kp2 = ("MacAddress", line[2].strip())
                    _kp3 = ("Link-Local-IPV6", line[3].strip())
                    _kp4 = ("IPV6 Address", line[4].strip())
                    key_pairs_data.append([_kp1, _kp2, _kp3, _kp4])

            output["ParameterValues"] = tuple(key_pairs_data)
            data_dictionary = self.__to_dictionary(output)
            return data_dictionary

    def dump_device_configurations_to_file(self):
        """
        Run all possible available commands that generate information about the device.
        Data will be stored in files .
        Each filename is a command, and the file' s data correspond to the output.
        Config the folder to store the files in Config.py
        :return: <int> 0
        """
        print("=" * 100)
        if self.Is_connected:

            # CHECK IF DUMP DIR EXISTS
            try:
                if not os.path.exists(self.__DIRNAME_DEVICE_DUMPS):
                    os.makedirs(self.__DIRNAME_DEVICE_DUMPS)
            except OSError as error:
                sys.exit(f"Error while attempting to create a folder {self.__DIRNAME_DEVICE_DUMPS} for device dump. "
                         f"\nError: {error}")

            # TODO .. BIG BULLSHIT. HERE
            #  CORRECT THIS
            for index, command in self.__MEO_DEVICE_COMMANDS.items():
                # For almmost all
                command_cleaned = replace_chars_from_cmds(command[0])

                print(yellow(f"OUTPUT - command_cleaned: {command_cleaned}"))
                dump_here_file_name = self.__DIRNAME_DEVICE_DUMPS + '/' + command_cleaned

                try:
                    if self.Is_connected:
                        print(f'OUTPUT - Sent command: {command[0]}')
                        data = self.send_command(command[0])
                        with open(dump_here_file_name, 'a') as fstream:
                            data = data.decode("UTF-8").replace("\r\n\n", "\n").split("\n")
                            for line in data:
                                fstream.write(line)
                except pexpect.ExceptionPexpect as error:
                    print(f'Failed when <- command: {command} \n Pexpect Error : {error}')
                    sys.exit(1)
                except Exception as error:
                    print(f'Failed when <- command: {command}. Exception Error: {error} ')
                    sys.exit("Bye bey ! ")
            print(green("[ DONE. Dump all device info in files ]"))
            return 0

    @classmethod
    def __to_dictionary(cls, data_to_convert) -> dict:
        """

        :param data_to_convert: <dict> dictionary with ... tuples ...and lists ... NOT GENERIC.
        :return: <dict>
        """
        inner_dictionary = {'Command': data_to_convert['Command'],
                            'Title': data_to_convert['Title']
                            }
        devices = {}

        for index, item in enumerate(data_to_convert['ParameterValues']):
            device = {"Device" + str(index): {}}

            for key_pairs in item:
                device["Device" + str(index)][key_pairs[0]] = key_pairs[1]
                # p rint(f"{key_pairs[0]}: {key_pairs[1]}")
                devices.update(device)
            # print('=' * 20)
        inner_dictionary['Devices'] = devices
        return inner_dictionary
    # TODO
    #  Generic? one

    @classmethod
    def __to_dictionary_diagnostics(cls, data_to_convert) -> dict:
        """

        :param data_to_convert: <dict> dictionary with ... tuples ...and lists ... NOT GENERIC.
        :return: <dict>
        """
        outer_dictionary = {"Command": data_to_convert['Command']}
        inner_dictionary = {'Title': data_to_convert['Title1']}
        devices = {}

        for index, item in enumerate(data_to_convert['ParameterValues1']):
            device = {"Device" + str(index): {}}

            for key_pairs in item:
                device["Device" + str(index)][key_pairs[0]] = key_pairs[1]
                # p rint(f"{key_pairs[0]}: {key_pairs[1]}")
                devices.update(device)
            # print('=' * 20)
        inner_dictionary['Devices'] = devices
        outer_dictionary['Lan'] = inner_dictionary
        del inner_dictionary
        del device
        # BREAK

        inner_dictionary = {'Title': data_to_convert['Title2']}
        devices = {}

        for index, item in enumerate(data_to_convert['ParameterValues2']):
            device = {"Device" + str(index): {}}

            for key_pairs in item:
                device["Device" + str(index)][key_pairs[0]] = key_pairs[1]
                # p rint(f"{key_pairs[0]}: {key_pairs[1]}")
                devices.update(device)
            # print('=' * 20)
        inner_dictionary['Devices'] = devices
        outer_dictionary['Wifi'] = inner_dictionary
        return outer_dictionary

    @classmethod
    def __to_dictionary_device_info(cls, data_to_convert) -> dict:
        """

        :param data_to_convert: <dict> dictionary with ... tuples ...and lists ... NOT GENERIC.
        :return: <dict>
        """
        inner_dictionary = {'Command': data_to_convert['Command'],
                            'Title': data_to_convert['Title']
                            }
        devices = {}

        for item in (data_to_convert['ParameterValues']):
            devices[item[0]] = item[1]

        inner_dictionary['DeviceInformation'] = devices
        return inner_dictionary