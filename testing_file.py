
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
        
        
    servo.duty_u16(int(((channel_packet[servo[1]]/100) * servo[3]) + servo[2]))
        

if channel_packet[7] >= 97:
    damcs(channel_packet)
    
