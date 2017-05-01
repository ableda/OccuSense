# OccuSense Senior Design Project

OccuSense is a room occupancy detection system that uses the thermal infrared sensor Melexis 90621 to count people entering and exiting each doorway. The system includes a user friendly web server hosted in Firebase to provide visualization of current and historical room occupancy and an easy way to combine multiple doorway subsystems into the same or different room. Each doorway has its own independent system which uses an Arduino for the I2C communication to extract the temperature values from the thermal sensor and passing them to a Raspberry Pi through USB serial port for data processing. The Raspberry Pi is also used as a central hub for networking with the server and includes a PIR (passive infrared) sensor as a reset mechanism, which sets the count back to zero when no motion is detected in the entire room after a long period of time.


Technical Background:

  The way that the system counts people is through processing the temperature frames that the sensor collects. The detection algorithm uses a threshold based on the frame's temperature spatial variance to determine if a person is present in a frame. It then buffers the person frames until one doesn't pass the threshold. A separate motion detection algorithm then runs on those buffered frames to determine direction the person is walking in. The program then sends the result to the server database where the room occupancy is updated.

  This algorithm works very effectively for individual doors, where usually only one person walks through at a time. To extend this for bigger doors a machine learning algorithm should probably be developed to distinguish multiple people in a frame and multiple simultaneous walk in and outs. The project contains all the data collection tools necessary to perform extensive research on the data and develop more complex algorithms on top of the already existing one.


This repository contains all the code necessary to replicate a door system and the firebase server. The main code to process data and detect/count people is hosted in the Raspberry Pi where most modifications and additions should be made. This repository offers all you need to get the data from the sensor using and Arduino through I2C communication. Getting the data straight from the Raspberry Pi turned out to be a very big challenge but it would be better. The repository also provides all the code necessary to replicate the user interface web server if desired. The following subsections describe some technical specifications and the contents of the repository folders.   

## Arduino

  Contains the library to extract the 16x4 temperature arrays in degrees Celsius. Includes a circuit diagram to properly set up the communication. The following principle of operation points describe how the temperature at each pixel is determined from the raw bytes extracted from the sensor.

  Principle of Operation:

    - Ta calculation

    - Pixel offset cancelling

    - Pixel to pixel sensitivity difference compensation

    - Object emissivity compensation

    - Object temperature calculation

  Here are the specifications for the main thermal sensor used by this system.

### Melexis 90621

      $40

      16x4 pixel IR array

      Field of view: 60° x 16°

      I2C compatible digital interface

      Programmable frame rate 0.5Hz…512Hz

      2.6V supply voltage, less than 9mA current consumption

      Datasheet:

      https://www.melexis.com/en/documents/documentation/datasheets/mlx90621


## Raspberry Pi

  The Raspberry Pi contains all the code used to parse and analyze the data as well as the communications to the server. It includes several python classes that are combined in one main class. The classes are meant to be easy to understand and use and can be easily extended to improve or use in different applications. The Raspberry Pi mainly communicates with the web server through the Firebase database, which can be easily checked and added to with a python firebase library. There are some other dependent libraries that must be installed in the Pi with pip, according to the imports in the main OccuSense class and the Raspberry_Pi folder readme.

  The Pi will also be the home to store raw data collected from the sensor. This data will be formatted in two different files. On one hand one file will store the raw temperature frames with a time stamp in a file named after the date. On the other it will store a file with the detections (a person walked in and out) with a time stamp, a value 1 or -1 and the amount of frames which passed the threshold. That way the user has the ability to visualize the underlying data and be able to perform more research on improving the existing algorithm or adjusting it for another application.

  Finally the Pi also hosts the PIR sensor for the reset mechanism, here are the specs.

### Parallax Wide Angle PIR Sensor

      Used for global reset to reset the count back to 0.

      Wide angle field of view 180º

      Voltage of 3V to 6V and current of 150 µA when idle and 3 mA when active.

      Easily connected to the Raspberry Pi GPIO pins.

      Datasheet:

      https://media.digikey.com/pdf/Data%20Sheets/Parallax%20PDFs/28032_Web.pdf


## Firebase Server

  The Firebase folder contains all the necessary code and instructions to deploy the same server that we currently have for the OccuSense system. The server is very important as it brings together all the independent sensor systems into rooms and serves as a great user friendly way to use the system. The independent sensor systems can also be used without a server, but extra code has to be added to keep room occupancy without the server. The sensor systems only send +1 and -1s to the server, not room counts. The server puts together the ins and outs of the different sensor systems in one room.
