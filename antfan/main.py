import time

from antfan.ant_com import AntNode
from antfan.controller import FanController
from antfan.hardware import DiscreteFan

if __name__ == "__main__":
    discreteFan = DiscreteFan()
    fanController = FanController(discreteFan)

    antnode = AntNode()
    antnode.add_heart_rate_monitor(fanController.heart_rate_data)
    print(f'init completed. starting ant communication')

    antnode.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    antnode.shutdown()
    discreteFan.disable_software_control()
    print(f'stopped.')
else:
    raise ImportError("Run this file directly, don't import it!")