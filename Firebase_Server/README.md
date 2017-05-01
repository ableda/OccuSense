# OccuSense Firebase Web Server

OccuSense Website:

+ Home
    + The homepage contains the navigation bar that lets you go to the setup screen or the room screen.
+ Setup
    + On the setup page, you can create a new sensor by selecting from a prepopulated list of available sensors (according to the firebase server) and then select an existing room to associate it with.
    + You can also create a new room to associate sensors with and you can set the room's maximum occupancy.
+ Rooms
    + On the rooms page, you can select the room you wish to view via the dropdown at the top of the page. The page will then refresh with the current and maximum occupancy of that room.
    + It will display the sensors associated with that room and will allow you to turn a sensor on/off, delete a sensor or start recording raw data from the sensor for a specified amount of time.
    + You can also see all the past historical data collected by the sensors for that room. Using the date dropdown, you can choose any day and view the average occupancy of the room per hour.

To Update the website on firebase:
+ Install NodeJs
+ Navigate to the directory containing all the website files using the "cd" command
+ Use the command "firebase init"
+ Unselect all the options except "Hosting"
+ Proceed with starting firebase
+ When prompted to create a new index.html, enter "N"
+ Use the command "firebase deploy" to deploy/update the website on firebase


The Firebase server is structured as follows:

+ (DD/MM/YYYY)
  + unique_id1
    + value: 1
    + time: 12:00 PM
    + sensor_id: 1122
  + unique_id2
    + value: -1
    + time: 12:05 PM
    + sensor_id: 1123
  + ..
+ sensors
  + 1122
    + on: 1
    + record: 0
    + record_time: 0
  + 1123
    + on: 1
    + record: 0
    + record_time: 0
+ rooms
  + PHO206
    + max_occupancy: 40
    + sensors: 1122, 1123
