from gpiozero import DigitalOutputDevice


# Represents a fan with discrete power levels.
# Power levels are controlled by setting GPIO2 for the lowest, GPIO 3 for mid and GPIO 4 for the highest level
class DiscreteFan:
    # GPIO pins
    outputs = [
        DigitalOutputDevice(2),
        DigitalOutputDevice(3),
        DigitalOutputDevice(4)
    ]

    def __init__(self):
        self.off()
        pass

    # sets outputs to false
    def off(self):
        for i in range(3):
            self.outputs[i].off()

    # sets the output corresponding to the given power_level to true and all other to false
    def set_power_level(self, power_level):
        if self.outputs[power_level - 1].value:
            return

        print(f'changing power level to {power_level}')
        for i in range(3):
            self.outputs[i].value = (power_level - 1 == i)
