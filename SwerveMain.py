# Import necessary modules
from machine import UART, Pin
import bluetooth
import time
import math
    
from XRPLib.defaults import *
from pestolink import PestoLinkAgent

from swervemodule import Module

#Choose the name your robot shows up as in the Bluetooth paring menu
#Name should be 8 characters max!
robot_name = "Diffy2"

# Create an instance of the PestoLinkAgent class
pestolink = PestoLinkAgent(robot_name)

uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17), timeout=40)

# U revers to "Upper" ie which gear is visable. L is lower gear
motor_AU = EncodedMotor.get_default_encoded_motor(index=1) # left motor
motor_BU = EncodedMotor.get_default_encoded_motor(index=2) # right motor
motor_AL = EncodedMotor.get_default_encoded_motor(index=3)
motor_BL = EncodedMotor.get_default_encoded_motor(index=4)

module_A = Module(motor_AU, motor_AL, -1)
module_B = Module(motor_BU, motor_BL, 1)

input_X = 127
input_Y = 127
input_Z = 127
last_ms = 0

def send_packet(data):
    payload = bytearray(data)
    length = len(payload)
    checksum = (sum(payload)) & 0xFF  # Simple checksum for validation
    packet = bytearray([0xAA, length]) + payload + bytearray([checksum])
    uart0.write(packet)

def read_packet():
    if uart0.any():
        # Check for the start byte
        if uart0.read(1) == b'\xAA':  
            length = uart0.read(1)[0]
            payload = uart0.read(length)
            checksum = uart0.read(1)[0]
            
            if checksum == (sum(payload)) & 0xFF:
                return payload
    return None

while True:

    # limit update frequency. 20 ms = 50 updates/s
    if (last_ms + 20 <= time.ticks_ms()):
        last_ms = time.ticks_ms()
        
        if pestolink.is_connected():  # Check if a BLE connection is established
    
            input_X = pestolink.get_raw_axis(0)
            input_Y = pestolink.get_raw_axis(1)
            input_Z = pestolink.get_raw_axis(2)
            
            send_packet([input_X, input_Y, input_Z])

        else: #default behavior when no BLE connection is open
            payload = read_packet()
            
            if (payload != None):
                input_X = payload[0]
                input_Y = payload[1]
                input_Z = payload[2]           

    true_X = (input_X / 127.5) - 1
    true_Y = (input_Y / 127.5) - 1
    
    module_A.go_to_target(true_X, true_Y)
    module_B.go_to_target(true_X, true_Y)
    #motor_AU.set_effort((input_X / 127.5) - 1)
    #motor_AL.set_effort((input_Y / 127.5) - 1)
    

    
    