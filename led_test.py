'''This code is made to be uploaded to the rasberry Pi. It is used to test if the Pi is reciving power.'''
from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)

while True:
    led.toggle()
    sleep(1)