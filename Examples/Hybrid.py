# Author: Colin Pollard
# Date: 6/25/2020
from Magnet import Magnet
from HallSensor import HallSensor
from Amplifier import Amplifier
from FieldCalculations import *
import matplotlib.pyplot as plt

# Create an example cylinder, 6mm diameter, 1mm thick, N52 grade
testCylinder = Magnet()
testCylinder.setCylinderSize(6, 1)
testCylinder.setGrade("N52")

DRV5055A1 = HallSensor(preset="DRV5055-A1")
DRV5055A4 = HallSensor(preset="DRV5055-A4")

LRAmplifier = Amplifier(preset="Diff-3.3-1.65-10")
LRAmplifier.setGain(50)

SRAmplifier = Amplifier(preset="Diff-3.3-1.65-10")
SRAmplifier.setGain(1)
sensors = [DRV5055A1, DRV5055A4]
amplifiers = [LRAmplifier, SRAmplifier]

distance, strength, voltages = sweepAmplifiedSensors(testCylinder, 1, 100, sensors, amplifiers)

fig, (ax1, ax2) = plt.subplots(2)
# Field Strength
ax1.plot(distance, strength, color='blue', linewidth=3)
ax1.set_title('Magnetic Field Strength')
ax1.set_ylabel('mT')
ax1.set_xlabel('mm')

# Voltages
for index in range(0, len(sensors)):
    ax2.plot(distance, voltages[index], linewidth=3, label=sensors[index].name)
ax2.legend()
ax2.set_title('Diff outputs')
ax2.set_ylabel('Volts')
ax2.set_xlabel('mm')
plt.show()
