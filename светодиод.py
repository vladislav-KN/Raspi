from RPi import GPIO 
from time import sleep 

GPIO.setmode(GPIO.BCM) 
GPIO.setup(23, GPIO.OUT) 

GPIO.output(23, True) 
sleep(5) 
GPIO.output(23, False) 
GPIO.cleanup()