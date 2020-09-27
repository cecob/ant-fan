from gpiozero import OutputDevice


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
        So R4 switches between 1=mechanical control (MC) and 0=software control (SC)
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
    __r4 = OutputDevice(12)

    def __init__(self):
        self.__last_power_level = None
        self.set_power_level(0)

    def disable_software_control(self):
        self.__r4.on()

    def enable_software_control(self):
        self.__r4.off()

    def set_power_level(self, power_level):

        if power_level == self.__last_power_level or power_level > 3 or power_level < 0:
            return None

        if self.__last_power_level is None:
            self.enable_software_control()

        print(f'changing power level to {power_level}')
        # reversed
        self.__last_power_level = power_level
        self.__r1.value = power_level == 0
        self.__r2.value = power_level == 2
        self.__r3.value = power_level == 1
