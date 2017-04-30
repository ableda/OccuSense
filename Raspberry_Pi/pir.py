import time
import firebase
from gpiozero import MotionSensor

firebase_url = 'https://occuserver.firebaseio.com/'

pir = MotionSensor(4)

time_to_reset = 60*60*2  #2 hours in seconds
start_time = time.time()

while True:
    if (time.time() - start_time) == time_to_reset:
        fire = firebase.FirebaseApplication(firebase_url, None)
        fire.patch('/sensors/' + str(self.sensorId), {'reset': 1})

    if pir.motion_detected:
        start_time = time.time()
