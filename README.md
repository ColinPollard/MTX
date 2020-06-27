# MTX
This software aims to provide a means of simulating combinations of magnetic fields, hall effect sensors, and outputted voltages through a combination of Magnet, Hall effect sensor, and Amplifier representations. Provides a simple and flexible way to simulate single, multiple, or combinations of magnets, sensors, and amplifiers. 

## Example Usage
Examples for simulating several configurations are available in the Examples directory. These leverage the fantastic library matplotlib for plotting of fields and voltages. If you desire a pure python example, simply comment the plotting methods which are at the bottom of each file.

**SensorExample.py** Demonstrates a sweeping simulation of 5 sensitivity variations of the DRV5055.
![](https://github.com/ColinPollard/MTX/blob/master/Examples/Pictures/SensorExample.PNG)

**Hybrid.py** Demonstrates a sweeping simulation of two different sensors each connected to a unique amplifier, with different gains.
![](https://github.com/ColinPollard/MTX/blob/master/Examples/Pictures/Hybrid.PNG)

## General procedure

**Each simulation will need a magnet instance as the source**, the process for creating a magnet is identical to the process for creating a sensor or an amplifier.
- Create a blank instance of a magnet
- Set the shape and size by calling one of the setSize methods. This will both configure the magnet to be the correct shape and size specified in one call.
- Set the strength through the setGrade method or by manually setting the remenance. This will be a physical magnet value provided by the manufacturer.
- You can now simulate magnetic field strength at a distance using calculate1DField()!

**If you want to simulate the voltage of a hall effect sensor some distance from a magnet**, you will need to create a hall effect sensor in addition to your magnet.
- Create either a blank instance of a HallSensor, or create one with a preset (if made from a preset, no further steps are needed.)
- Set the type of the sensor to be bipolar or unipolar at your desired voltage.
- Set the range of the sensor in milliTeslas
- Set the sensitivity of the sensor
- You can now simulate the voltage output of a sensor using either the built in sensor function or using the wrapper calculateVoltage1D().
  - If using the built in method, you will need to calculate the magnetic field strength, and pass it into the sensor.voltage(fieldStrength) method. This will return the sensor's estimated voltage output.
  - If using the calculateVoltage1D, simply pass it a magnet, sensor, and distance and it will return the voltage of the sensor at that distance.

**If you want to simulate the voltage of a sensor connected through an op amp,** you will need a magnet, sensor, and amplifier instance.
- Create either a blank instance of Amplifier, or create one from a preset.
- Set the type of amplifier
- Set the range of the amplifier
- Set the gain of the amplifier if needed (not needed for log amps)
- Now simulate the voltage output by passing an input voltage into amplifierInstance.vOut(vIn)

## Simulations (FieldCalculations.py)
Field calculations houses all of the simulation types, these are a variety of sweeping, and fixed simulations. Generally each one works the same way, pass it a magnet, and the sensor(s)/amplifier(s) and it will return both a list of X position values, and voltages. Some return multiple voltages for several sensors, others do not. The docstrings very well explain how each one works.

By returning the distance on each simulation, it allows easy plotting when an x-axis is needed.

## Magnets (Magnet.py)
This class is designed to represent a magnet with a shape, size, and strength.

**Shape:**
- Cylinder
- Cubic
- Ring
- Sphere

**Strength:**
- Conversion from standard "N" grades - N35 to N52
- Custom Gauss remanence

**Size**
- Fully customizable sizing of magnet, for each shape configuration.

## Sensors (HallSensor.py)
This class is designed to represent and estimate hall effect sensor performance.

**Presets**
- Sensor instances can be created with a preset parameter in the constructor. This sets all of the parameters of the sensor to a know value.
- After a sensor is created from a preset, all values are still modifiable.
- Currently available presets:
  - DRV5055-A1 through DRV5055-A5

**Type**
- Type of sensor is configurable to be either bipolar or unipolar at a either 3.3v or 5v. Easy to add new models for voltage estimation. Currently the TI DRV5055 is used as the base model.

**Sensitivity:**
- Sensitivity is fully configurable, and entered in milliVolts per milliTesla
- Range of sensors can be configured in either min/max field strength, or min/max voltage. Whichever is limiting is used in voltage calculations. Can be configured to be symmetrical (+-range) or double ended.

## Amplifiers (Amplifier.py)
This class is designed to represent and estimate Op-Amp performance. Can easily be used in conjunction with sensor instances to simulate amplified hall effect sensors.

**Presets**
- Using the same system as for HallSensor.py, amplifiers can be created using a preset parameter in the constructor. Values are still modifiable after creation from a preset, and presets are easy to create.
- Currently available presets are very limited and are there primarily to demonstrate how more can be implemented.

**Type**
- Non-Inverting
- Inverting
- Differential Amplifier
- Logarithmic Amplifier
- Differential Logarithmic Amplifier
 
 **Voltage Clipping**
 - Minimum and maximum output voltage are specified and determine the point at which the output will clip.
 - If using a rail to rail amplifier, these voltages will simply be the supply voltages, otherwise be sure to include the voltage drop.
