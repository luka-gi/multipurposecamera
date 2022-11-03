import time
import Jetson.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

mode="BOARD"
_gpio_mode="BOARD" 

channels = [13,15,16,18]


direction= 16     # Direction -> GPIO Pin
step = 18

print(GPIO.getmode())
degree = 1.8
resolution = (0,0,1,1)
steps=200
clockwise= False

stepdelay=0.1
mode_pins= channels
direction_pin=direction
step_pin=step
GPIO.setup(channels, GPIO.OUT)
GPIO.setup(direction_pin, GPIO.OUT)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(mode_pins, GPIO.OUT)
GPIO.output(direction_pin,True)
for i in range(steps):
    
    time.sleep(stepdelay)
    GPIO.output(channels, resolution)
    time.sleep(stepdelay)
    GPIO.output(step_pin, False)
    time.sleep(stepdelay)
    GPIO.output(step_pin, True)




