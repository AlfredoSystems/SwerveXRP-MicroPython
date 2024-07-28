# Import necessary modules
from machine import UART, Pin
import bluetooth
import time
import math
    
from XRPLib.defaults import *
from pestolink import PestoLinkAgent

from swerveModule import Module

#Choose the name your robot shows up as in the Bluetooth paring menu
#Name should be 8 characters max!
robot_name = "SwerveX"

# Create an instance of the PestoLinkAgent class
pestolink = PestoLinkAgent(robot_name)

uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

# U revers to "Upper" ie which gear is visable. L is lower gear
motor_AU = EncodedMotor.get_default_encoded_motor(index=1) # left motor
motor_BU = EncodedMotor.get_default_encoded_motor(index=2) # right motor
motor_AL = EncodedMotor.get_default_encoded_motor(index=3)
motor_BL = EncodedMotor.get_default_encoded_motor(index=4)

module_A = Module(motor_AU, motor_AL, -1)
module_B = Module(motor_BU, motor_BL, 1)

input_X = 0
input_Y = 0
last_ms = 0

while True:

    # limit to 5 fps
    if (last_ms + 20 <= time.ticks_ms()):
        last_ms = time.ticks_ms()
        
        if pestolink.is_connected():  # Check if a BLE connection is established
    
            input_X = pestolink.get_raw_axis(0)
            input_Y = pestolink.get_raw_axis(1)
            
            data = bytearray([input_X, input_Y])
            uart0.write(data)

        else: #default behavior when no BLE connection is open
            if (uart0.any() > 0):
                data_in = uart0.read(2)

                #print("Data contents: ", ' '.join(f'0x{byte:02x}' for byte in data_in))

                input_X = data_in[0]
                input_Y = data_in[1]
                
                #print(str(input_X) + " " + str(input_Y))

    true_X = (input_X / 127.5) - 1
    true_Y = (input_Y / 127.5) - 1
    
    module_A.go_to_target(true_X, true_Y)
    module_B.go_to_target(true_X, true_Y)
    #motor_AU.set_effort((input_X / 127.5) - 1)
    #motor_AL.set_effort((input_Y / 127.5) - 1)

    
    
