# OccuSense Senior Design Project

OccuSense is a room occupancy detection system that uses the thermal infrared sensor Melexis 90621 to count people entering and exiting each doorway. The system includes a user friendly web server hosted in Firebase to provide visualization of current and historical room occupancy and an easy way combine multiple doorway subsystems into the same or different rooms. Each doorway has its own independent system which uses an Arduino for the I2C communication to extract the temperature values from the thermal sensor and a Raspberry Pi as a central hub for data processing, networking with the server and includes a PIR (passive infrared) sensor as a reset mechanism, which sets the count back to zero when no motion is detected in the entire room after a long period of time.

This repository contains all the code necessary to replicate a door system and the firebase server, the following subsections provide background and guidelines to using the code.     


Melexis 90621:
  16x4 pixel IR array
  Field of view: 60°x16°
  I2C compatible digital interface
  Programmable frame rate 0.5Hz…512Hz
  2.6V supply voltage, less than 9mA current consumption

  add link to datasheet

Arduino I2C communication:

  Library to extract the 16x4 temperature array in degrees Celsius. Corresponds to one frame.  

  Principle of Operation:
  􀁸 Ta calculation
  􀁸 Pixel offset cancelling
  􀁸 Pixel to pixel sensitivity difference compensation
  􀁸 Object emissivity compensation
  􀁸 Object temperature calculation


Raspberry Pi Central Hub:

  Occusense class is the main class for data processing into counting and/or data collection. The data collection corresponds in creating a text file with temperature array frame with a time stamp. Utilizes the dataCollection and motionDetection classes.

  Main: this is the file that is running constantly checking database entries to determine what to do. The options are adding sensors to rooms, start or stop each sensor
