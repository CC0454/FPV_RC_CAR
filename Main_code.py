from machine import PWM, Pin, UART
from time import sleep, sleep_us

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

hardware_list = [[motor, 2, 3333, 2633], [servo, 0, 3166, 3167],[reverse, 4, 3333, 2633]]


def push_to_hardware(channel_packet):
    for device in hardware_list:
        for index, channel in enumerate(channel_packet):
            if index == device[1]:
                pwm = int(((channel/100) * device[3]) + device[2])
                device[0].duty_u16(pwm)
                

def format_channel(channel_input):
    formatted_channel_list = []
    
    for i in channel_input:
        rounded_channel = int(100 * ((i - 173) / 1637))
        formatted_channel_list += [rounded_channel]
    #174 / 1811 
    #print_channel(formatted_channel_list)
    return formatted_channel_list


def print_channel(formatted_channel_list):
    print_string = ""
    for formatted_channel in formatted_channel_list:
        print_string += str(formatted_channel)
        print_string += "% | "
        
    print(print_string)


def decode(parent):
    if len(parent) < 10:
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
    
    return format_channel([channel1, channel2, channel3, channel4, channel5, channel6, channel7, channel8])
    

    
while True:
    formatted_channels = "none"
    if uart1.read(1) == b'\x16':
        
        payload = uart1.read(24)
        if payload != b'':
            formatted_channels = decode(payload)
            push_to_hardware(formatted_channels)
    
    sleep_us(100)
    
    
    
   