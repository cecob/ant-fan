from ant.core import driver
from ant.core.exceptions import ANTException
from ant.core.node import Node, Network
from ant.core.constants import NETWORK_KEY_ANT_PLUS, NETWORK_NUMBER_PUBLIC
from ant.plus.heartrate import *
import os

class AntNode:
    deviceProfile: [DeviceProfile] = []

    def __init__(self):
        os.system("usbreset 001/002")
        self.node = Node(driver.USB2Driver())
        self.network = Network(key=NETWORK_KEY_ANT_PLUS, name='N:ANT+')
        pass

    def add_heart_rate_monitor(self, on_data_received):
        heart_rate_monitor = HeartRate(self.node, self.network, {'onHeartRateData': on_data_received})
        self.deviceProfile.append(heart_rate_monitor)

    def start(self):
        try:
            self.node.start()
            self.node.setNetworkKey(NETWORK_NUMBER_PUBLIC, self.network)
            for profile in self.deviceProfile:
                profile.open()
            print('ANT started. Connecting to devices...')
        except ANTException as err:
            print(f'Could not start ANT.\n{err}')

    # ya you better call these or you may have to unplug the antnode+ stick
    def shutdown(self):
        for profile in self.deviceProfile:
            profile.close()
        self.node.stop()
