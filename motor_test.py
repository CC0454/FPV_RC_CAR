'''This code is used to test ESC PWM ranges.'''
from machine import Pin, PWM
from time import sleep

motor = PWM(Pin(4))
motor.freq(50)

range = 100
base = 3333
max = 5966 - base



while True:
    #angle to pwm:
    precentage = int(input("Precentage\n>"))
    pwm = int(((precentage/range) * max) + base)
    motor.duty_u16(pwm)
    print(pwm)
     

# Motor range: 3333 - 5966