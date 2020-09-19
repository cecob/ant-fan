from gpiozero import OutputDevice


# Represents a fan with 3 discrete power levels.
#
# Power levels can be chosen mechanically with buttons on the fan or via the software.
# The fan itself is controlled by rewiring the incoming AC to one of 3 inputs (PL1, PL2, PL3)
# To control the rewiring we use the 3 relays R1, R2 and R3.
# R1 switches between 0=mechanical control (MC) and 1=software control (SC)
# R2 and R3 are used to set the SC power level, with their binary encoded state represent the PL
# 00=1, 01=1, 10=2, 11=3
#      AC
#      |
#  R1 _/ ____
#   |        |
#  MC        SC
#            |
#        R2 _/ ____
#           |      |
#           | R3 _/ _
#           |    |   |
#          PL1  PL2  PL3
class DiscreteFan:
    # GPIO pins
    __SC = OutputDevice(2)
    __lsb = OutputDevice(3)
    __msb = OutputDevice(4)

    def __init__(self):
        self.__last_power_level = None
        self.set_power_level(0)

    def disable_software_control(self):
        self.__SC.off()

    def enable_software_control(self):
        self.__SC.on()

    def set_power_level(self, power_level):
        if power_level > 3 | power_level < 0 | power_level == self.__last_power_level:
            return

        print(f'changing power level to {power_level}')
        self.__last_power_level = power_level
        self.__SC.value = power_level > 0
        self.__lsb.value = power_level != 2
        self.__msb.value = power_level != 1
