# Author: Colin Pollard
# Date: 6/24/2020
# This class represents an amplifier, designed to handle hall effect sensor inputs.
import math


class Amplifier:
    """
    Amplifier representation.
    """
    def __init__(self, preset=None):
        """
        Create a new amplifier, optionally from a preset.

        :param preset: name of preset
        :type preset: string
        """
        # Type of amplifier (non-inverting, differential)
        self.__type = None
        self.__gain = None
        self.__diffVoltage = None
        self.__vMin = self.__vMax = None
        # Log amplifier parameters
        self.__vt = self.__is = self.__r = None

        # If no preset is selected, the parameters are kept as None
        if preset is None:
            pass

        # Differential rail to rail op amp with 3.3v supply, diff voltage at 1.65v, and gain of 2
        elif preset == "Diff-3.3-1.65-10":
            self.setType("diff", diffVoltage=1.65)
            self.setGain(10)
            self.setRange(0, 3.3)
        # Differential log rail to rail op amp with +-3.3v supply, diff voltage at 1.65, 1n4004 diode
        elif preset == "DiffLog-3.3-1.65":
            self.setType("diffLog", diffVoltage=1.65)
            self.setRange(-3.3, 3.3)
            self.__vt = .026
            self.__is = .000000007
            self.__r = 100
        else:
            raise ValueError("Unrecognized preset. Check syntax.")

    def setType(self, type, diffVoltage=None, vt=None, isat=None, logR=None):
        """
        Set the type of op amp.
        Differential amplifiers require the diffVoltage to be set to the positive terminal voltage.
        Logarithmic amplifiers require the diode characteristics to be set.

        :param type: type of amplifier
        :type type: string
        :param diffVoltage: positive terminal voltage to be subtracted
        :type diffVoltage: float
        :param vt: Thermal voltage of diode for logarithmic amplifiers (most likely 26mV) in Volts
        :type vt: float
        :param isat: Saturation current of the diode for logarithmic amplifiers.
        :type isat: float
        :param logR: Input resistor to logarithmic amplifier.
        :type logR: float
        :return: None
        :raises ValueError: If a special configuration is requested, but no required parameters are detected.
        """

        # Differential amplifier requires the voltage to offset by
        if type == "diff" or type == "diffLog":
            if diffVoltage is None:
                raise ValueError("Differential op amp selected, but no diffvoltage was provided.")
            else:
                self.__diffVoltage = diffVoltage

        # Log amplifier requires diode and resistor characteristics
        elif type == "log" or "diffLog":
            if vt is None or isat is None or logR is None:
                raise ValueError("Log amp was selected but diode characteristics were not provided.")
            else:
                self.__vt = vt
                self.__is = isat
                self.__r = logR

        self.__type = type

    def setGain(self, gain):
        """
        Set the gain of the op amp.

        :param gain: Gain of the op amp in Volts/Volt
        :type gain: float
        :return: None
        """
        self.__gain = gain

    def setRange(self, min, max):
        """
        Set the voltageRange.

        :param min: Minimum achievable output voltage.
        :type min: float
        :param max: Maximum achievable output voltage.
        :type max: float
        :return: None
        """
        self.__vMin = min
        self.__vMax = max

    def vOut(self, vIn):
        """
        Calculates a voltage output given an input voltage.

        :param vIn: Input voltage
        :type vIn: float
        :return: Output voltage
        :raises AttributeError: If the type of amplifier is not set, or if the type is set but other information such as gain is missing.
        :raises ValueError: If the set gain is unnachievable for the type of amplifier.
        """
        # Error check type, gain, voltage
        if self.__type is None:
            raise AttributeError("Type of amplifier not specified. Please select a type first.")
        elif self.__gain is None:
            # If the amplifier is logarithmic, there is no traditional gain
            if not self.__type == "diffLog":
                raise AttributeError("Gain of amplifier not specified. Please select a gain first.")
        elif self.__vMin is None:
            raise AttributeError("Voltage range not specified. Please select a voltage first.")

        # Calculate theoretical voltage without clipping
        if self.__type == "diff":
            vOut = (vIn - self.__diffVoltage) * self.__gain

        # Logarithmic amplifier with differential input
        elif self.__type == "diffLog":
            if self.__vt is None:
                raise ValueError("To use a logarithmic amplifier, please enter the diode characteristics first.")
            else:
                vOut = -self.__vt * math.log((vIn - self.__diffVoltage) / (self.__is * self.__r))

        # Log amplifier
        elif self.__type == "log":
            if self.__vt is None:
                raise ValueError("To use a logarithmic amplifier, please enter the diode characteristics first.")
            else:
                vOut = -self.__vt * math.log((vIn) / (self.__is * self.__r))

        # Non inverting gain can never be below unity
        elif self.__type == "noninv":
            if self.__gain < 1:
                raise ValueError("Invalid gain setting for non inverting op amp")
            else:
                vOut = vIn * self.__gain

        # Inverting must always be negative, but can be a fraction
        elif self.__type == "inv":
            if self.__gain >= 0:
                raise ValueError("Invalid gain setting for inverting op amp")
            else:
                vOut = vIn * self.__gain

        # Unrecognized type
        else:
            raise AttributeError("Invalid amplifier type selected.")

        # Check for clipping
        if vOut > self.__vMax:
            vOut = self.__vMax
        if vOut < self.__vMin:
            vOut = self.__vMin

        return vOut
