import statistics
import time

from antfan import logger
from antfan.hardware import DiscreteFan
from bikecomputer.bikecomputer import BikeComputer, DataSeries


def map_to_power_level(computed_heart_rate):
    if computed_heart_rate > 155:
        return 3
    elif computed_heart_rate > 140:
        return 2
    elif computed_heart_rate > 120:
        return 1
    return 0


if __name__ == "__main__":
    fan = DiscreteFan()
    computer = BikeComputer(20, DataSeries.HEART_RATE).start()

    while True:
        try:
            time.sleep(5)
            # fan should switch up faster that it would switch down
            avg_hr_5_sec = computer.map_reduce(DataSeries.HEART_RATE, 5, statistics.mean)
            avg_hr_10_sec = computer.map_reduce(DataSeries.HEART_RATE, 10, statistics.mean)
            pl_5_sec = map_to_power_level(avg_hr_5_sec)
            pl_10_sec = map_to_power_level(avg_hr_10_sec)

            logger.debug(f'avg 5s HR: {avg_hr_5_sec} -> PL {pl_5_sec} '
                         f'avg 10s HR: {avg_hr_10_sec} -> PL {pl_5_sec}')

            if pl_5_sec > fan.current_power_level:
                fan.set_power_level(pl_5_sec)
            else:
                fan.set_power_level(pl_10_sec)

        except KeyboardInterrupt:
            break

    computer.stop()
    logger.info('stopped')
else:
    raise ImportError("Run this file directly, don't import it!")
