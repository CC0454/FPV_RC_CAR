from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(2))
servo.freq(50)

range = 100
base = 0
max = 65535 - base

while True:
    #angle to pwm:
    precentage = int(input("Precentage\n>"))
    pwm = int(((precentage/range) * max) + base)
    print(pwm)
    servo.duty_u16(pwm)

#range = 0- 65535