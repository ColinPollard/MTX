# Author: Colin Pollard
# Date: 6/24/2020
# This class represents a magnet, and will store all needed data for simulations


class Magnet:
    """
    Magnet representation.
    """
    def __init__(self):
        # Type of magnet
        self.__shape = None
        # Dimensions
        self.__length = self.__width = self.__thickness = self.__diameter = self.__iDiameter = None
        # Strength
        self.__grade = self.__remanence = None

    def setGrade(self, grade):
        """
        Set the grade of the magnet instance to a known preset.
        Sets remanence accordingly.

        :param grade: Magnet grade ex: N52
        :type grade: string
        :return: None
        """
        # Convert from standard grades to remanence (br) in Gauss
        if grade == "N35":
            self.__remanence = 12000
        elif grade == "N38":
            self.__remanence = 12400
        elif grade == "N40":
            self.__remanence = 12700
        elif grade == "N42":
            self.__remanence = 13000
        elif grade == "N45":
            self.__remanence = 13500
        elif grade == "N48":
            self.__remanence = 14000
        elif grade == "N50":
            self.__remanence = 14300
        elif grade == "N52":
            self.__remanence = 14600
        else:
            raise ValueError("Unrecognized grade preset. Please set remenance manually.")
        self.__grade = grade

    def setRemanence(self, br):
        """
        Set the remanence of the magnet manually. Does not affect grade.
        :param br: remanence of the magnet in gauss.
        :type br: float
        :return: None
        """
        self.__remanence = br

    def setCylinderSize(self, diameter, thickness):
        """
        Configures the magnet to be a cylinder, sets size.

        :param diameter: Diameter of the cylinder.
        :type diameter: float
        :param thickness: Thickness or height of the cylinder.
        :type thickness: float
        :return: None
        """
        self.__shape = "cylinder"
        self.__diameter = diameter
        self.__thickness = thickness
        # Set other dimensions to None
        self.__length = None
        self.__width = None
        self.__iDiameter = None

    def setCubicSize(self, length, width, thickness):
        """
        Configures the magnet to be a cubic, sets size.

        :param length: Length of the magnet.
        :type length: float
        :param width: Width of the magnet.
        :type width: float
        :param thickness: Thickness or height of the magnet.
        :type thickness: float
        :return: None
        """
        self.__shape = "cubic"
        self.__length = length
        self.__width = width
        self.__thickness = thickness
        # Set unused dimensions to none
        self.__diameter = None
        self.__iDiameter = None

    def setRingSize(self, diameter, iDiameter, thickness):
        """
        Configures the magnet to be a ring, sets size.

        :param diameter: Outside diameter of the ring.
        :type diameter: float
        :param iDiameter: Inner diameter of the ring.
        :type iDiameter: float
        :param thickness: Thickness or height of the ring.
        :type thickness: float
        :return: None
        """
        self.__shape = "ring"
        self.__diameter = diameter
        self.__iDiameter = iDiameter
        self.__thickness = thickness
        # Set unused dimensions to None
        self.__length = None
        self.__width = None

    def setSphereSize(self, diameter):
        """
        Configures the magnet to be a sphere, sets size.

        :param diameter: Diameter of the sphere.
        :type diameter: float
        :return: None
        """
        self.__shape = "sphere"
        self.__diameter = diameter
        # Set unused dimensions to None
        self.__iDiameter = None
        self.__thickness = None
        self.__length = None
        self.__width = None

    def shape(self):
        """
        Gets the shape of the magnet.

        :return: Shape of magnet
        :rtype: string
        :raises AttributeError: If the shape is not configured.
        """
        if self.__shape is None:
            raise AttributeError("Shape not configured. Please set the size before using.")
        return self.__shape

    def getCylinderSize(self):
        """
        Gets the size of the magnet when it is configured as a cylinder.

        :return: diameter, thickness/height
        :rtype: tuple[float, float]
        :raises AttributeError: If the magnet is not configured as a cylinder.
        """
        if self.__diameter is None:
            raise AttributeError("The magnet is not currently configured as a Cylinder. Double check that the setCylinderSize has been called.")
        return self.__diameter, self.__thickness

    def getCubicSize(self):
        """
        Gets the size of the magnet when it is configured as a cubic.

        :return: length, width, thickness/height
        :rtype tuple[float, float, float]
        :raises AttributeError: If the magnet is not configured as a cubic.
        """
        if self.__length is None:
            raise AttributeError("The magnet is not currently configured as a Cubic. Double check that the setCubicSize has been called.")
        return self.__length, self.__width, self.__thickness

    def getRingSize(self):
        """
        Gets the size of the magnet when it is configured as a ring.

        :return: outer diameter, inner diameter, thickness/height
        :rtype tuple[float, float, float]
        :raises AttributeError: If the magnet is not configured as a ring.
        """
        if self.__iDiameter is None:
            raise AttributeError(
                "The magnet is not currently configured as a Ring. Double check that the setRingSize has been called.")
        return self.__diameter, self.__iDiameter, self.__thickness

    def getSphereSize(self):
        """
        Gets the size of the magnet when it is configured as a sphere.

        :return: diameter
        :rtype float
        :raises AttributeError: If the magnet is not configured as a sphere.
        """
        if self.__diameter is None:
            raise AttributeError(
                "The magnet is not currently configured as a Sphere. Double check that the setSphereSize has been called.")
        return self.__diameter

    def getStrengthGauss(self):
        """
        Gets the strength of the magnet in gauss.

        :return: remanence in gauss.
        :rtype float
        :raises AttributeError: If the magnet has no strength set.
        """
        if self.__remanence is None:
            raise AttributeError("The strength of this magnet has not been set yet. Call setGrade with a known preset, or manually set with setRemenence.")
        return self.__remanence

    def getStrengthMT(self):
        """
        Gets the strength of the magnet in milliTeslas.

        :return: remanence in mT.
        :rtype float
        :raises AttributeError: If the magnet has no strength set.
        """
        if self.__remanence is None:
            raise AttributeError("The strength of this magnet has not been set yet. Call setGrade with a known preset, or manually set with setRemenence.")
        return self.__remanence / 10000