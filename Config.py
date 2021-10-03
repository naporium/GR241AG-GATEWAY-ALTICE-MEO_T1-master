import os


class Config():

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
    # print(os.path.join(ROOT_DIR, 'DeviceDumpDir'))

    HOSTNAME = os.environ.get('MEO_REMOTE_HOSTNAME') or '192.168.1.254'
    USERNAME = os.environ.get('MEO_FG_USERNAME') or 'meo'
    PASSWORD = os.environ.get('MEO_FG_PASSWD') or 'meo'

    # pexpect Logs: if set to true will log to file the stdout pexpect interaction to file below.
    PEXPECT_LOG_ENABLED = True
    PEXPECT_LOG_FILENAME = 'Meo_device_pexpect.log'

    # FOR DUMPING ALL DEVICE CONFIGURATIONS IN FILE TEXTS.... THIS IS THE LOCATION
    # We can parse from files instead...
    DIRNAME_DEVICE_DUMPS = os.environ.get('MEO_CONFIGURATIONS_DUMP_DIR') or 'DeviceDumpDir'