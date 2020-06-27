# Author: Colin Pollard
# Date: 6/24/2020
from Core.Magnet import Magnet
from Core.HallSensor import HallSensor
from Core.Amplifier import Amplifier
import math


def calculate1DField(magnet, distance):
    """
    Calculates the magnetic field strength at a given distance away from a magnet.

    :param magnet: Magnet to simulate
    :type magnet: Magnet
    :param distance: Distance between magnet and point.
    :type distance: float
    :return: Field density in mT
    :rtype: float
    """

    # Type check that the magnet is a Magnet.py instance
    if not isinstance(magnet, Magnet):
        raise ValueError("Magnet provided is not a valid Magnet.py instance.")

    # Determine magnet shape
    if magnet.shape() == "cylinder":
        diameter, thickness = magnet.getCylinderSize()
        radius = diameter / 2
        # Calculate field strength, B
        B = (magnet.getStrengthMT() / 2) * (((thickness + distance) / math.sqrt(radius ** 2 + (thickness + distance) ** 2)) - (distance / math.sqrt(radius ** 2 + distance ** 2)))

    elif magnet.shape() == "cubic":
        length, width, thickness = magnet.getCubicSize()
        B = (magnet.getStrengthMT() / math.pi) * \
            (math.atan((length * width) / (2 * distance * math.sqrt(4 * distance ** 2 + length ** 2 + width ** 2)))
             - math.atan((length * width) / (2 * (thickness + distance) * math.sqrt(4 * (thickness + distance) ** 2 + length ** 2 + width ** 2))))

    elif magnet.shape() == "ring":
        diameter, iDiameter, thickness = magnet.getRingSize()
        outerRadius = diameter / 2
        innerRadius = iDiameter / 2
        B = (magnet.getStrengthMT() / 2) * (((thickness + distance)/(math.sqrt(outerRadius ** 2 + (thickness + distance) ** 2))) -
                                            (distance / (math.sqrt(outerRadius ** 2 + distance ** 2))) -
                                            (((thickness + distance) / (math.sqrt(innerRadius ** 2 + (thickness + distance) ** 2))) -
                                             (distance / (math.sqrt(innerRadius ** 2 + distance ** 2)))))
    elif magnet.shape() == "sphere":
        diameter = magnet.getSphereSize()
        radius = diameter / 2
        B = magnet.getStrengthMT() * (2 / 3) * ((radius ** 3) / ((radius + distance) ** 3))

    else:
        raise NotImplementedError("Type of magnet not recognized for this field calculation. Double check the type of magnet is set.")
    # The equations used to calculate the field can be found at: https://www.supermagnete.de/eng/faq/How-do-you-calculate-the-magnetic-flux-density
    return B


def calculateVoltage1D(magnet, sensor, distance):
    """
    Calculates a sensor voltage output from a 1D magnetic field.

    :type sensor: HallSensor
    :param sensor: Sensor to simulate.
    :type magnet: Magnet
    :param magnet: Magnet to simulate.
    :return: Voltage output of sensor.
    :rtype: float
    """
    B = calculate1DField(magnet, distance)
    # Convert from Teslas to mT
    B = B * 1000
    voltage = sensor.voltage(B)
    return voltage


def sweepMagnet(magnet, startDistance, endDistance):
    """
    Runs a sweep simulation of a magnet, calculates field at 10 points per 1 distance.

    :param magnet: Instance of a Magnet to sweep
    :type magnet: Magnet
    :param startDistance: Starting distance
    :type startDistance: float
    :param endDistance:  Ending distance
    :type endDistance: float
    :return: list of distance values (x-axis), list of field strength.
    :rtype: tuple[list[float], list[float]]
    """
    distance = []
    strength = []

    # Increment by 10s
    for index in range(startDistance * 10, endDistance * 10):
        distanceMM = index / 10
        distance.append(distanceMM)  # Save distance
        field = calculate1DField(magnet, distanceMM) * 1000
        strength.append(field)  # Save Field Strength

    return distance, strength


def sweepSensor(magnet, startDistance, endDistance, sensor):
    """
    Runs a sweep simulation of a single magnet and sensor.

    :param magnet: Magnet to simulate.
    :type magnet: Magnet
    :param startDistance: Starting distance
    :type startDistance: float
    :param endDistance:  Ending distance
    :type endDistance: float
    :param sensor: Sensor to simulate.
    :type sensor: HallSensor
    :return: List of distance values (x-axis), list of field strength, list of sensor voltage.
    :rtype: tuple[list[float], list[float], list[float]]
    """
    voltage = []
    distance = []
    strength = []

    # Increment by 10s
    for index in range(startDistance * 10, endDistance * 10):
        distanceMM = index / 10
        distance.append(distanceMM)  # Save distance
        field = calculate1DField(magnet, distanceMM) * 1000
        strength.append(field)  # Save Field Strength
        voltage.append(sensor.voltage(field))

    return distance, strength, voltage


def sweepSensors(magnet, startDistance, endDistance, sensors):
    """
    Runs a sweep simulation of a magnet and set of sensors.

    :param magnet: Magnet to simulate.
    :type magnet: Magnet
    :param startDistance: Starting distance
    :type startDistance: float
    :param endDistance:  Ending distance
    :type endDistance: float
    :param sensors: List of sensors to simulate
    :type sensors: list[HallSensor]
    :return: List of distance values (x-axis), list of field strength, list of list of sensor voltage.
    :rtype: tuple[list[float], list[float], list[list[float]]]
    """

    voltages = []
    # The voltages array must have the correct number of lists in it based on the number of sensors
    for index in range(0, len(sensors)):
        voltages.append([])

    distance = []
    strength = []

    # Increment by 10s
    for index in range(startDistance * 10, endDistance * 10):
        distanceMM = index / 10
        distance.append(distanceMM)  # Save distance
        field = calculate1DField(magnet, distanceMM) * 1000
        strength.append(field)  # Save Field Strength
        # Calculate voltages
        for sensorIndex in range(0, len(sensors)):
            voltages[sensorIndex].append(sensors[sensorIndex].voltage(field))

    return distance, strength, voltages


def sweepAmplifiedSensor(magnet, startDistance, endDistance, sensor, amplifier):
    """
    Runs a sweep simulation of a set of sensors, each connected to a unique amplifier.

    :param magnet: Magnet to simulate.
    :type magnet: Magnet
    :param startDistance: Starting distance
    :type startDistance: float
    :param endDistance:  Ending distance
    :type endDistance: float
    :param sensor: Sensors to simulate
    :type sensor: HallSensor
    :param amplifier: Amplifiers to simulate
    :type amplifier: Amplifier
    :return: List of distance values (x-axis), list of field strength, list of sensor voltages.
    :rtype: tuple[list[float], list[float], list[float]]
    """

    voltage = []
    distance = []
    strength = []

    # Increment by 10s
    for index in range(startDistance * 10, endDistance * 10):
        distanceMM = index / 10
        distance.append(distanceMM)  # Save distance
        field = calculate1DField(magnet, distanceMM) * 1000
        strength.append(field)  # Save Field Strength
        voltage.append(amplifier.vOut(sensor.voltage(field)))

    return distance, strength, voltage


def sweepAmplifiedSensors(magnet, startDistance, endDistance, sensors, amplifiers):
    """
    Runs a sweep simulation of a set of sensors, each connected to a unique amplifier.

    :param magnet: Magnet to simulate.
    :type magnet: Magnet
    :param startDistance: Starting distance
    :type startDistance: float
    :param endDistance:  Ending distance
    :type endDistance: float
    :param sensors: List of sensors to simulate
    :type sensors: list[HallSensor]
    :param amplifiers: List of amplifiers to simulate
    :type amplifiers: list[Amplifier]
    :return: List of distance values (x-axis), list of field strength, list of list of sensor voltages.
    :rtype: tuple[list[float], list[float], list[list[float]]]
    """

    voltages = []
    # The voltages array must have the correct number of lists in it based on the number of sensors
    for index in range(0, len(sensors)):
        voltages.append([])

    distance = []
    strength = []

    # Increment by 10s
    for index in range(startDistance * 10, endDistance * 10):
        distanceMM = index / 10
        distance.append(distanceMM)  # Save distance
        field = calculate1DField(magnet, distanceMM) * 1000
        strength.append(field)  # Save Field Strength
        # Calculate voltages
        for sensorIndex in range(0, len(sensors)):
            voltages[sensorIndex].append(amplifiers[sensorIndex].vOut(sensors[sensorIndex].voltage(field)))

    return distance, strength, voltages