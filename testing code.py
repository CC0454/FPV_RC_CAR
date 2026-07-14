from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(2))
servo.freq(50)

while True:
    #angle to pwm:
    angle = int(input("Angle\n>"))
    pwm = int(((angle/180) * 6000) + 2000)
    print(pwm)
    servo.duty_u16(pwm)

#range = 2000 - 8000