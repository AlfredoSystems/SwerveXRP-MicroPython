# Import necessary modules
from machine import Pin 
import math
from Vector2D import Vector2D
from XRPLib.defaults import *

class Module:
    TICKS_PER_MODULE_REV = 12 * (48 / 1) * (74 / 36) * 2  # ticks per MODULE revolution
    DEGREES_PER_TICK = 360 / TICKS_PER_MODULE_REV

    TICKS_PER_WHEEL_REV = 12 * (48 / 1) * (74 / 36) * (11 / 45)

    ALLOWED_MODULE_ORIENTATION_ERROR = 10  # degrees
    ANGLE_OF_MAX_MODULE_ROTATION_POWER = 30  # degrees
    ROT_ADVANTAGE = 1  # max rotation power divided by max translation power (scaling factor)
    MAX_MOTOR_POWER = 1

    def __init__(self, motor_AU, motor_AL, encoder_sign):
        self.takingShortestPath = False
        self.moduleReversed = False
        self.motor_AU = motor_AU
        self.motor_AL = motor_AL
        self.encoder_sign = encoder_sign
        self.move_component = 0
        self.pivot_component = 0

    def get_azimuth(self):
        azimuth = (self.motor_AU.get_position_counts() + self.motor_AL.get_position_counts()) * self.DEGREES_PER_TICK * self.encoder_sign
        return azimuth

    def get_pivot_component(self, target_angle):
        current_angle = self.get_azimuth()
        
        angle_diff = abs(current_angle - target_angle) % 360
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
            
        fixed_angle = ((current_angle + 180) % 360) - 180
        delta = ((target_angle - fixed_angle + 180) % 360) - 180

        if abs(angle_diff) > 110:  # Was 90
            if not self.takingShortestPath:
                self.moduleReversed = not self.moduleReversed  # Reverse translation direction because module is newly reversed
            self.takingShortestPath = True
        else:
            self.takingShortestPath = False

        if angle_diff > self.ANGLE_OF_MAX_MODULE_ROTATION_POWER:
            angle_diff = self.ANGLE_OF_MAX_MODULE_ROTATION_POWER
        
        if angle_diff < self.ALLOWED_MODULE_ORIENTATION_ERROR:
            direction = 0
        else:
            direction = (1 if delta >= 0 else -1) * angle_diff / self.ANGLE_OF_MAX_MODULE_ROTATION_POWER * self.ROT_ADVANTAGE
        
        
        #print("{:.2f} {:.2f} {:.2f} {:.2f}".format(target_angle, current_angle, fixed_angle, direction))
        
        return direction

    def set_motors(self, drivePower, aziPower):
        MOTOR_1_VECTOR = Vector2D(1 / math.sqrt(2), 1 / math.sqrt(2))
        MOTOR_2_VECTOR = Vector2D(-1 / math.sqrt(2), 1 / math.sqrt(2))
        
        drivePower = max(min(drivePower, 1), -1)

        powerVector = Vector2D(drivePower, aziPower)
        motor1Unscaled = powerVector.project_to(MOTOR_1_VECTOR)
        motor2Unscaled = powerVector.project_to(MOTOR_2_VECTOR)

        motor1power = math.copysign(abs(motor1Unscaled), motor1Unscaled.y)
        motor2power = math.copysign(abs(motor2Unscaled), motor2Unscaled.y)
        
        maxUnscaledMotor = max(abs(motor1power), abs(motor2power))
        if maxUnscaledMotor > self.MAX_MOTOR_POWER:
            motor1power = self.MAX_MOTOR_POWER * motor1power / maxUnscaledMotor
            motor2power = self.MAX_MOTOR_POWER * motor2power / maxUnscaledMotor
        
        self.motor_AU.set_effort(motor1power * self.encoder_sign)
        self.motor_AL.set_effort(motor2power * self.encoder_sign)

    def go_to_target(self, input_X, input_Y):
        target_vector = Vector2D(1 * input_X, -1 * input_Y)
        
        if (self.moduleReversed):
            target_vector = target_vector * -1

        self.move_component = abs(target_vector)
        if self.moduleReversed:
            self.move_component *= -1
        
        target_angle = target_vector.to_deg()
        if abs(target_vector) >= 0.05:
            self.pivot_component = self.get_pivot_component(target_angle)
        else:
            self.pivot_component = self.get_pivot_component(self.get_azimuth())


        self.set_motors(self.move_component, self.pivot_component)
