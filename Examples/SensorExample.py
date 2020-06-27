# Author: Colin Pollard
# Date: 6/24/2020
from Core.FieldCalculations import *
import matplotlib.pyplot as plt  # you do not need this import if you comment out the plotting code below and want a pure python example.

# Create an example cylinder, 6mm diameter, 1mm thick, N52 grade
testCylinder = Magnet()
testCylinder.setCylinderSize(6, 1)
testCylinder.setGrade("N52")

# Create an example cubic, 6mm length, 6mm width, 6mm thick, N35
testCubic = Magnet()
testCubic.setCubicSize(6, 6, 6)
testCubic.setGrade("N35")

# Create an example ring, 6mm OD, 3mm ID, 6mm thick, N38
testRing = Magnet()
testRing.setRingSize(6, 3, 6)
testRing.setGrade("N38")

# Create an example sphere, 6mm diameter, N40
testSphere = Magnet()
testSphere.setSphereSize(6)
testSphere.setGrade("N40")

# Calculate field at 10mm
d10Cy = calculate1DField(testCylinder, 10)
print(d10Cy)  # In teslas, to convert to mT multiply by 1000.
d10Cu = calculate1DField(testCubic, 10)
print(d10Cu)
d10Cr = calculate1DField(testRing, 10)
print(d10Cr)
d10Cs = calculate1DField(testSphere, 10)
print(d10Cs)

# Now we can calculate voltage by creating a sensor and evaluating it.
DRV5055A1 = HallSensor()
DRV5055A1.setType("bipolar3.3")
# Bipolar operation means the range is symmetrical +-21mT
DRV5055A1.setSymRange(21)
# 100mV/mT
DRV5055A1.setSensitivity(100)
vA1 = calculateVoltage1D(testCylinder, DRV5055A1, 10)
print(vA1)

# We can also use one of the presets in the HallSensor class to skip the setup above for certain models.
DRV5055A2 = HallSensor(preset="DRV5055-A2")
vA2 = calculateVoltage1D(testCylinder, DRV5055A2, 1)
print(vA2)

# Create an array of sensors to sweep
sensors = [HallSensor(preset="DRV5055-A1"), HallSensor(preset="DRV5055-A2"), HallSensor(preset="DRV5055-A3"), HallSensor(preset="DRV5055-A4"), HallSensor(preset="DRV5055-A5")]
# Run a sweep simulation of sensor list
distance, strength, voltages = sweepSensors(testCylinder, 1, 100, sensors)

# Plot the results as a function of distance (comment this to avoid using matplotlib)
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
ax2.set_title('Sensor Voltage Output')
ax2.set_ylabel('Volts')
ax2.set_xlabel('mm')
plt.show()
