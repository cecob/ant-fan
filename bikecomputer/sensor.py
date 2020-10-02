from dataclasses import dataclass
from enum import Enum

from ant.core.node import ChannelID


class DataSeries(Enum):
    HEART_RATE = 1
    RR_INTERVAL = 2


@dataclass
class Sensor:
    name: str
    capabilities: [DataSeries]
    ant_channel_id: ChannelID


'''
we dont want to pair every time the fan starts, so we hardcode the sensor's channel
'''
wahoo_heart_rate_sensor = Sensor(
    "Wahoo HR",
    [DataSeries.HEART_RATE, DataSeries.RR_INTERVAL],
    ChannelID(12955, 120, 1)
)
