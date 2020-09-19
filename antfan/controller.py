from antfan.hardware import DiscreteFan


def map_to_power_level(computed_heart_rate):
    if computed_heart_rate > 150:
        return 3
    elif computed_heart_rate > 130:
        return 2
    elif computed_heart_rate > 100:
        return 1
    return 0


class FanController:
    fan: DiscreteFan

    def __init__(self, fan: DiscreteFan):
        self.fan = fan

    def heart_rate_data(self, computed_heartrate, event_time_ms, rr_interval_ms):
        print(f'Heart rate: {computed_heartrate}')
        power_level = map_to_power_level(computed_heartrate)
        self.fan.set_power_level(power_level)
