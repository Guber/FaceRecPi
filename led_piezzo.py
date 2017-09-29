import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 100)

def toggleLed(pin, state):
    GPIO.output(pin,state)

def buzzOn():
    GPIO.output(18, True) 
    p.start(100)             # start the PWM on 100  percent duty cycle  
    p.ChangeDutyCycle(90)   # change the duty cycle to 90%  
    p.ChangeFrequency(261) 

def buzzOff():
    p.stop()
    
def cleanup():
    GPIO.cleanup()
