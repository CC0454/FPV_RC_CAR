from machine import Pin, UART
from time import sleep, sleep_us

uart1 = UART(0, baudrate=420000, tx=Pin(0), rx=Pin(1))

print_throttle = 0
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
    byte4 = parent[3]
    byte5 = parent[4]
    byte6 = parent[5]
    byte7 = parent[6]
    byte8 = parent[7]
    byte9 = parent[8]
    byte10 = parent[9]
    byte11 = parent[10]
    
    
    # Roll
    channel1 = (byte1 | (byte2 << 8)) & 0x07FF
    
    # Pitch
    channel2 = ((byte2 >> 3) | (byte3 << 5)) & 0x7FF
    
    # Throttle
    channel3 = ((byte3 >> 6) | (byte4 << 2) | (byte5 <<10)) & 0x7FF
    
    # Yaw
    channel4 = ((byte5 >> 1) | (byte6 << 7)) & 0x7FF
        
    # SA
    channel5 = ((byte6 >> 4) | (byte7 << 4)) & 0x7FF
    
    # SB
    channel6 = ((byte7 >> 7) | (byte8 << 1) | (byte9 << 9)) & 0x7FF
    
    # SC
    channel7 = ((byte9 >> 2) | (byte10 << 6)) & 0x7FF
    
    # SD
    channel8 = ((byte10 >> 5) | (byte11 << 3)) & 0x7FF
    
    print_channel([channel1, channel2, channel3, channel4, channel5, channel6, channel7, channel8])
    

    
while True:
    if uart1.read(1) == b'\x16':
        
        payload = uart1.read(24)
        if payload != b'':
            decode(payload)
            
    sleep_us(100)
    
    
    
