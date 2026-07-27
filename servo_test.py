'''This code is used to test servo PWM ranges'''
from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(5))
servo.freq(50)

range = 180
base = 2000
max = 8000 - base

while True:
    #angle to pwm:
    angle = int(input("Angle\n>"))
    pwm = int(((angle/range) * max) + base)
    print(pwm)
    servo.duty_u16(pwm)

#range = 2000 - 8000