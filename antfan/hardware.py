from time import sleep

from gpiozero import OutputDevice, DigitalOutputDevice

from antfan import logger


class DiscreteFan:
    """
        Represents a fan with 3 discrete power levels.
        Power levels can be chosen mechanically with buttons on the fan or via the software.
        The fan itself is controlled by rewiring the incoming AC to one of 3 inputs (PL1, PL2, PL3)
        To control the rewiring we use the 4 NC-relays R1, R2, R3 and R4.

                         AC
                          |
                    R1 _1/ 0______
                     |           |
               R4 _1/ 0_         |
                 |     |         |
                MC    off   R2 _1/ 0____
                              |        |
                              |  R3 _1/ 0_
                              |     |    |
                             PL2   PL1  PL3

        Layout is mainly due to place restriction inside of the AC-Box of the fan and is designed to
        use the MC in case the program is not running.
        So R4 switches between 1=mechanical control (MC) and 0=software control (SC).
        Note: R4 is hardwired to GND so its always off as long as the pi is powered

        R2 and R3 are used to set the power level as:
        R2 | R3 || PL
         0 | 0  || 3
         0 | 1  || 1
         1 | 0  || 2
         1 | 1  || 2

    """
    # GPIO pins
    __r1 = OutputDevice(16)
    __r2 = OutputDevice(20)
    __r3 = OutputDevice(21)

    def __init__(self):
        self.current_power_level = None
        self.set_power_level(0)

    def say_hallo(self):
        logger.info('hi')
        self.__r3.value = True
        sleep(0.25)
        self.__r2.value = True
        sleep(0.25)
        self.__r3.value = False
        sleep(0.25)
        self.__r2.value = False


    def set_power_level(self, power_level):
        if power_level == self.current_power_level or power_level > 3 or power_level < 0:
            return None

        logger.info(f'changing power level to {power_level}')
        self.current_power_level = power_level
        self.__r1.value = power_level == 0
        self.__r2.value = power_level == 2
        self.__r3.value = power_level == 1
