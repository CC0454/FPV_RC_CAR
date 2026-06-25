from machine import Pin, UART
from time import sleep, sleep_us

uart1 = UART(0, baudrate=420000, tx=Pin(0), rx=Pin(1))

def print_channel(channel_input):
    print_string = ""
    for i in channel_input:
        rounded_channel = int(100 * ((i - 173) / 1637))
        print_string += str(rounded_channel)
        print_string += "% | "
    print(print_string)
    #174 / 1811

def decode(parent):
    if len(parent) < 2:
        return
    
    byte1 = parent[0]
    byte2 = parent[1]
    byte3 = parent[2]
    
    channel1 = (byte1 | (byte2 << 8)) & 0x07FF
    
    
    channel2 = ((byte2 >> 3) | (byte3 << 5)) & 0x7FF
    
    print_channel([channel1, channel2])
    

    
while True:
    if uart1.read(1) == b'\x16':
        
        payload = uart1.read(24)
        if payload != b'':
            decode(payload)
            
    sleep_us(100)
    
    
    
