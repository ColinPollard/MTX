# Author: Colin Pollard
# Date: 6/24/2020
from Magnet import Magnet
from HallSensor import HallSensor
from Amplifier import Amplifier
from FieldCalculations import calculate1DField, calculateVoltage1D
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

# Create an example sensor, DRV5055-A1
testSensor = HallSensor(preset="DRV5055-A1")

# Create lists to store raw voltage and amplified voltage
sensorVoltage = []
amplifierVoltage = []
logAmplifierVoltage = []
postLogAmplifierVoltage = []
distance = []
strength = []

# .1 to 100mm in increments of 0.1mm (index must be whole numbers, so we divide to create .1 increments)
for index in range(1, 1000):
    distanceMM = index / 10
    distance.append(distanceMM)
    # Calculate field strength
    strength.append(calculate1DField(testCylinder, distanceMM))
    # Calculate raw sensor voltage, store to list
    sensorV = calculateVoltage1D(testCylinder, testSensor, distanceMM)
    sensorVoltage.append(sensorV)
    # Calculate and store amplifier output
    amplifierVoltage.append(testAmplifier.vOut(sensorV))
    # Logarithmic diff amplifier followed by diff non inverting
    logAmplifierVoltage.append(logAmplifier.vOut(sensorV))
    postLogAmplifierVoltage.append(diffAmplifier.vOut(logAmplifier.vOut(sensorV)))


# Plot the results as a function of distance (comment this to avoid using matplotlib)
fig, (ax1, ax2, ax3) = plt.subplots(3)

# Field Strength
ax1.plot(distance, strength, color='blue', linewidth=3)
ax1.set_title('Magnetic Field Strength')
ax1.set_ylabel('mT')
ax1.set_xlabel('mm')
ax1.xaxis.set_label_coords(.5, -0.025)

ax2.plot(distance, sensorVoltage, label='DRV5055-A1')
ax2.plot(distance, amplifierVoltage, label='Amplified 10x diff (1.65v)')
ax2.legend()
ax2.set_title('Sensor Voltage Output')
ax2.set_ylabel('Volts')
ax2.set_xlabel('mm')
ax2.xaxis.set_label_coords(.5, -0.025)

ax3.set_title('Logarithmic Amplifier')
ax3.plot(distance, logAmplifierVoltage, label='log diff (1.65v)')
ax3.plot(distance, postLogAmplifierVoltage, label='diff of log diff 10x (-0.377v)')
ax3.legend()
ax3.set_ylabel('Volts')
ax3.set_xlabel('mm')
ax3.xaxis.set_label_coords(.5, -0.025)

#plt.tight_layout()
plt.show()
