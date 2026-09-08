'''This code is used to drve a rasberry Pi powered car'''
# Main imports
from machine import PWM, Pin, UART
from time import sleep, sleep_us

# ELRS / CRSF UART Pin import
uart1 = UART(0, baudrate=420000, tx=Pin(0), rx=Pin(1))

# Servo range: 3166 - 6333
servo = PWM(Pin(2))
servo.freq(50)

# Motor range: 3333 - 5966
motor = PWM(Pin(3))
motor.freq(50)

  
# Reverse range: 3333 - 5966
reverse = PWM(Pin(4))
reverse.freq(50)

# A list of external hardware, Format [[varible, allocated channel, min PWM, PWM range (max - min)]]
hardware_list = [[motor, 2, 3333, 2633], [servo, 0, 3166, 3167],[reverse, 4, 3333, 2633]]

def damcs(channel_packet):
    # This is the function that runs DAMCS (Dual axi motion control system).
    # It works by sensing the stick position and changing the calculations for the PWM output accordingly. 
    
    motor = hardware_list[0]
    reverse = hardware_list[2]
    servo = hardware_list[1]
    
    if channel_packet[2] < 45:
        reverse[0].duty_u16(3333)
        motor[0].duty_u16(int(((1 - (channel_packet[2] / 50)) * motor[3]) + motor[2]))
        
        
    elif channel_packet[2] >= 55:
        reverse[0].duty_u16(5966)
        motor[0].duty_u16(int((((channel_packet[2] - 50) / 50)  * motor[3]) + motor[2]))
        
    else:
        motor[0].duty_u16(3333)
               
    servo[0].duty_u16(int(((channel_packet[servo[1]]/100) * servo[3]) + servo[2]))

def push_to_hardware(channel_packet):
    print(channel_packet[2])
    # This funciton converts channels to PWM then pushes it to the external hardware.
    
    if channel_packet[7] >= 97:
        damcs(channel_packet)
        print("damcs running")
    else:
        for device in hardware_list:
            pwm = int(((channel_packet[device[1]]/100) * device[3]) + device[2])
            device[0].duty_u16(pwm)


def format_channel(channel_input):
    # This funcition takes raw bit input and formats it to a precentage from 0 to 100
    formatted_channel_list = []
    
    for i in channel_input:
        rounded_channel = int(100 * ((i - 173) / 1637))
        formatted_channel_list += [rounded_channel]
    #174 / 1811 
    #print_channel(formatted_channel_list)
    return formatted_channel_list


def print_channel(formatted_channel_list):
    # This function is used for debuging and prints out the precentages of all channels.
    print_string = ""
    for formatted_channel in formatted_channel_list:
        print_string += str(formatted_channel)
        print_string += "% | "
        
    print(print_string)


def decode(parent):
    # this funciton takes the packet, dissects it into a raw data list and sends it to the format_channel funcition to get formatted
    if len(parent) < 11:
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
    
    push_to_hardware(format_channel([channel1, channel2, channel3, channel4, channel5, channel6, channel7, channel8]))
    

while True:
    #This is the mainloop 
    formatted_channels = "none"
    if uart1.read(1) == b'\x16':
        
        payload = uart1.read(24)
        if payload != b'':
            decode(payload)

    sleep_us(100)
     