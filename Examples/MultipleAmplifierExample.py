# Author: Colin Pollard
# Date: 6/24/2020
from Core.Magnet import Magnet
from Core.HallSensor import HallSensor
from Core.Amplifier import Amplifier
from Core.FieldCalculations import calculate1DField, calculateVoltage1D
import matplotlib.pyplot as plt  # you do not need this import if you comment out the plotting code below and want a pure python example.

# Create an example cylinder, 6mm diameter, 1mm thick, N52 grade
testCylinder = Magnet()
testCylinder.setCylinderSize(6, 1)
testCylinder.setGrade("N52")

# Create an example amplifier, differential, 3.3v rail to rail, gain of 2, diff voltage at 1.65
testAmplifier = Amplifier(preset="Diff-3.3-1.65-10")
# Differential log amplifier to try to linearize signal
logAmplifier = Amplifier(preset="DiffLog-3.3-1.65")
# Diff non-inverting amplifier for second stage log
diffAmplifier = Amplifier()
diffAmplifier.setRange(-3.3, 3.3)
diffAmplifier.setType("diff", diffVoltage=-0.377)
diffAmplifier.setGain(10)


# Now we can create a list of field strength and voltage per distance
distance = []
strength = []
sensors = [HallSensor(preset="DRV5055-A1"), HallSensor(preset="DRV5055-A2"), HallSensor(preset="DRV5055-A3"), HallSensor(preset="DRV5055-A4")]
amplifiers = []
voltages = []
# The voltages array must have the correct number of lists in it based on the number of sensors
for index in range(0, len(sensors)):
    voltages.append([])

# .1 to 100mm in increments of 0.1mm (index must be whole numbers, so we divide to create .1 increments)
for index in range(1, 2000):
    distanceMM = index / 10
    distance.append(distanceMM)  # Save distance
    strength.append(calculate1DField(testCylinder, distanceMM) * 1000)  # Save Field Strength
    # Calculate voltages
    for sensorIndex in range(0, len(sensors)):
        voltages[sensorIndex].append(diffAmplifier.vOut(logAmplifier.vOut(calculateVoltage1D(testCylinder, sensors[sensorIndex], distanceMM))))

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
ax2.set_title('Log to Diff output')
ax2.set_ylabel('Volts')
ax2.set_xlabel('mm')
plt.show()