from time import time

from ant.core import driver
from ant.core.exceptions import ANTException
from ant.core.node import Node, Network, ChannelID
from ant.core.constants import NETWORK_KEY_ANT_PLUS, NETWORK_NUMBER_PUBLIC
from ant.plus.heartrate import *

import os

from antfan import logger
from bikecomputer.sensor import Sensor


class DeviceManager:
    """
    provides basic logging for an ant device connection
    """

    def __init__(self, device_profile: DeviceProfile, channel_id: ChannelID):
        self.channel_id = channel_id
        self.device_profile = device_profile
        self.device_profile.callbacks.update({
            'onSearchTimeout': lambda x: logger.warn(f'search for {device_profile.name} timed out'),
            'onDevicePaired': lambda x, y: logger.info(f'Connected to {device_profile.name} ({channel_id})'),
            'onChannelClosed': lambda x: logger.info(f'Channel closed for {device_profile.name}')
        })

    def open(self):
        logger.info(f'searching for device on channel: {self.channel_id}...')
        self.device_profile.open(channelId=self.channel_id, searchTimeout=255 * 2.5)

    def close(self):
        logger.info(f'closing communication channel {self.channel_id}')
        self.device_profile.close()


class AntNode:
    deviceManager: [DeviceManager] = []

    def __init__(self):
        os.system("usbreset 0fcf:1008")
        self.node = Node(driver.USB2Driver())
        self.network = Network(key=NETWORK_KEY_ANT_PLUS, name='N:ANT+')

    def add_heart_rate_monitor(self, sensor: Sensor, on_data_received):
        device = DeviceManager(
            HeartRate(self.node, self.network, {'onHeartRateData': on_data_received}),
            sensor.ant_channel_id
        )
        self.deviceManager.append(device)

    def start(self):
        try:
            self.node.start()
            self.node.setNetworkKey(NETWORK_NUMBER_PUBLIC, self.network)
            logger.info('ANT started. Connecting to devices...')
            for profile in self.deviceManager:
                profile.open()
        except ANTException as err:
            logger.info(f'Could not start ANT.\n{err}')

    # ya you better call these or you may have to unplug the antnode+ stick
    def shutdown(self):
        for profile in self.deviceManager:
            profile.close()
        self.node.stop()
