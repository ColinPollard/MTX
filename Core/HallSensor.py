# Author: Colin Pollard
# Date: 6/24/2020
# This class represents a basic hall effect sensor


class HallSensor:
    """
    Hall effect sensor representation.
    """
    def __init__(self, preset=None):
        """
        Creates a new Hall effect sensor. If a preset exists for the sensor, the preset attribute will set all parameters.

        :param preset: preset name
        :type preset: string
        """
        if preset is None:
            self.__sensitivity = None
            self.__maxRange = self.__minRange = None
            self.__type = None
            self.name = None
        # Presets for the DRV5055 series at 3.3v. For a different voltage, manually create one as shown in the example.
        elif preset == "DRV5055-A1":
            self.name = "DRV5055-A1"
            self.setType("bipolar3.3")
            self.setSensitivity(100)
            self.setSymRange(21)
        elif preset == "DRV5055-A2":
            self.name = "DRV5055-A2"
            self.setType("bipolar3.3")
            self.setSensitivity(50)
            self.setSymRange(42)
        elif preset == "DRV5055-A3":
            self.name = "DRV5055-A3"
            self.setType("bipolar3.3")
            self.setSensitivity(25)
            self.setSymRange(85)
        elif preset == "DRV5055-A4":
            self.name = "DRV5055-A4"
            self.setType("bipolar3.3")
            self.setSensitivity(12.5)
            self.setSymRange(169)
        elif preset == "DRV5055-A5":
            self.name = "DRV5055-A5"
            self.setType("bipolar3.3")
            self.setSensitivity(-100)
            self.setSymRange(21)
        else:
            raise NotImplementedError("The desired preset does not exist... yet. Double check your syntax against the HallSensor constructor.")

    def setSensitivity(self, mVmT):
        """
        Sets the sensitivity in milliVolts per milliTesla

        :param mVmT: sensitivity in mV/mT
        :return: None
        """
        self.__sensitivity = mVmT / 1000

    def setRange(self, min, max):
        """
        Sets the range to two unique values (good for unipolar where the minimum is 0)

        :param min: Minimum sensible field strength in mT
        :type min: float
        :param max: Maximum sensible field strength in mT
        :type max: float
        :return: None
        """
        self.__minRange = min
        self.__maxRange = max

    def setSymRange(self, input):
        """
        Sets the range equal to +-input (good for bipolar sensors)

        :param input: Minimum/maximum sensible field strength in mT
        :type input: float
        :return: None
        """
        self.__maxRange = input
        self.__minRange = -input

    def setType(self, inputType):
        """
        Sets the type of sensor (unipolar, bipolar) does not error check input

        :param inputType: sensor type
        :type inputType: string
        :return: None
        """
        self.__type = inputType

    def getSensitivity(self):
        """
        Gets the sensitivity of the sensor in mV/mT

        :return: sensitivity of sensor
        :rtype float
        """
        if self.__sensitivity is None:
            raise AttributeError("No sensitivity set. Please call setSensitivity first.")
        return self.__sensitivity

    def getRange(self):
        """
        Gets the range of the sensor in mT

        :return: minimum range, maximum range
        :rtype tuple[float, float]
        """
        if self.__minRange is None:
            raise AttributeError("No range set. Please call setRange or setSymRange first.")
        return self.__minRange, self.__maxRange

    def voltage(self, field):
        """
        Calculates the output voltage for a given field strength in mT

        :param field: field strength in mt.
        :type field: float
        :return: voltage
        :rtype float
        """
        if self.__type == "bipolar3.3":
            # These calculations are based on a DRV5055 running at 3.3v
            vQ = 3.3 / 2
            vOut = vQ + field * self.__sensitivity

            # Check for clipping (0.2 volts are limits to linear range for this sensor)
            if vOut > 3.3 - 0.2 or field > self.__maxRange:
                vOut = 3.3 - 0.2
            elif vOut < 0.2 or field < self.__minRange:
                vOut = 0.2

        elif self.__type == "bipolar5":
            # These calculations are based on a DRV5055 running at 3.3v
            vQ = 5 / 2
            vOut = vQ + field * self.__sensitivity

            # Check for clipping
            if vOut > 4.8 or field > self.__maxRange:
                vOut = 4.8
            elif vOut < 0.2 or field < self.__minRange:
                vOut = 0.2

        elif self.__type == "unipolar3.3":
            vOut = field * self.__sensitivity

            # Check for clipping based on field range, may create strange behavior at limits.
            # Checking by voltage range may work better, but YMMV
            if vOut > 3.1 or field > self.__maxRange:
                vOut = 3.1
            elif vOut < 0.2 or field < self.__minRange:
                vOut = 0.2

        elif self.__type == "unipolar5":
            vOut = field * self.__sensitivity

            # Check for clipping - same note as above
            if vOut > 4.8 or field > self.__maxRange:
                vOut = 4.8
            elif vOut < 0.2 or field < self.__minRange:
                vOut = 0.2

        return vOut
