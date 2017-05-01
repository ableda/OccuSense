# MLX90621 Library

This folder includes the code necessary to extract the 16x4 temperature frames from the Melexis 90621 via I2C and utilizing the Wire Arduino library. It also includes a diagram schematic of the circuit connections for proper usage.

All you need is the Arduino IDE program to be able to upload this program into any Arduino board. Arduino Software link: https://www.arduino.cc/en/Main/Software

### wireMLX90621:

The wireMLX90621 is the class header file. This is the main file to look at to understand what is required to do to read in the temperature array. Most constants and the resource behind this code is from the Melexis 90621 datasheet which is also in this folder. The principle of operation as to how the temperatures are extracted from the raw bytes is described in the next section. 


### MLX90621:

The MLX90621 is the implementation file for the wireMLX90621 header file. In this file it is more clear how the code translates the raw bytes to temperatures in Celsius. Essentially, the first step is to read the sensor's EEPROM memory to get important constants for later calculations. The order of how the functions that are called to then get a frame is clear in the measure function in line 17.
After reading the EEPROM, it writes the trimming value and sets the sensor configurations like the frame rate. After it reads the PTAT (Proportional To Absolute Temperature) sensor which is integrated to measure the ambient temperature of the chip. It then reads the IR values of each pixel. Then the appropiate calculations are made to translate the value to a temperature in Celsius.

Principle of Operation:

  - Ta calculation

  - Pixel offset cancelling

  - Pixel to pixel sensitivity difference compensation

  - Object emissivity compensation

  - Object temperature calculation


### mlx90621:

This .ino file is the main file, depends on the previous two files. It is essentially the running file which utilizes the wireMLX90621 class to read in and values and print them in the serial port, so they can be read by a computer or in this case a raspberry pi for processing.  
