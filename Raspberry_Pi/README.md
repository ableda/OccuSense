# Raspberry Pi Programs Python

This folder contains the main classes and programs necessary to make the system work. It provides with all the code necessary to run the OccuSense system with the Raspberry Pi connected to the Arduino via serial port as described in the Arduino folder and with the PIR reset mechanism as described by the PIR_Schematic picture attached here. These are all python files for version 2.7. Some of the dependencies of these files are the following libraries: numpy, requests, json, threading, firebase, PIL, gpiozero and serial. These can all be installed by using the command "pip install" +  the name of the module to install. The following paragraphs describe each main class and its function in relation to the project.

It is important to note that the serial port of the Raspberry Pi can only be accessed by one process at a time. All the code is designed based on this restriction.


### Occusense

Occusense.py is the main class for this project. This is the class that puts it all together. One thread is constantly reading the serial port and processing the temperature frames. On a separate thread it is constantly checking the web server for possible action changes or changes of operation. The final thread runs the pir reset mechanism (the pir.py file is an independent version if you wish to run the reset mechanism as another process). The threads communicate with each other through the class variables which they all have access to. These must be on separate threads because checking the server takes to long to do between reading frames (it would tremendously slow down the frame rate). This class is dependent on the data collection and the motion detection classes.

From the server you can control the program state. Data Collection or Normal Mode. In the data collection state the program saves all the temperature frames from the sensor as well as the detection history both marked with time stamps. In the default state, the program just processes the frames and sends to the server if someone walked in or out. It determines the state by checking entries in the firebase database. More options and functions can be easily added by adding more entries to the database and updating the web server to update the database accordingly.

In order to run the program without the server, the database check thread should be cancelled by passing a False as the third argument in the initializer function, this also cancels the pir reset mechanism. As default the program would just print a +1 or -1 every time someone walks in or out without pushing anything to the server.

The Raspberry pi has a daemon on startup that runs main.py, which initializes an instance of this class to run with a specific sensor id (each raspberry pi should initialize this class with a different sensor id).


### motionDetection

This is the class that contains the motion detection algorithm. It is created so that the main Occusense class could be simpler and easier to understand. The motion detection algorithm works on an input of a number of frames. These frames are determined by the threshold. This algorithm is based on the cross correlation array between the time series array of the hottest pixel in the first frame to the other 63 time series arrays of the other pixels. It is described in more detail in the User's manual in the reports folder. The only dependency is the python numpy library.


### dataCollection

This is the class used to collect data, or to save the raw frames and the detections in text files for later inspection and research. This class is used by the main Occusense class. It can also be used independently to save raw data and detections. It is necessary as a separate class from the Occusense because of the restriction that the serial port can only be accessed by one process at a time.

The collect_data.py file is the program to run offline to collect data if you do not want to use the server. It prompts for the number of seconds you want to collect data for. Each file is named based on the day it was created so you cannot have more than 24 hours of data in the same file. Detection files follow the same pattern for simplicity.
