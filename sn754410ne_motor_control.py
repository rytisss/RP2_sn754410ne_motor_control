from machine import Pin, PWM
import time


class SN754410NE_motor:
    def __init__(self, backward_pin: int, forward_pin: int, soft_step = 100, soft_time_ms = 10) -> None:
        """
        backward_pin - pin id
        forward_pin - pin id
        soft_step - step in the resolution [0;65535] according to which the motor control will increase accordingly
        soft_time_ms - time for each 'soft_step' in miliseconds
        """
        self.__backward_pin = backward_pin
        self.__forward_pin = forward_pin
        # setup pins for PWM generation
        self.__pin_forward = Pin(forward_pin, mode=Pin.OUT)
        self.__pin_backward = Pin(backward_pin, mode=Pin.OUT)
        # setup PWM mode for these pins
        self.__pin_forward_pwm = PWM(self.__pin_forward)
        self.__pin_backward_pwm = PWM(self.__pin_backward)
        # stop at the beginning
        self.stop_instant()
    
    # Raspberry pico duty cycle resolution is 16bits [0;65535]
    # This function converts [1;100] to [0;65535]
    def percent_to_rp_duty(self, percentage: int) -> int:
        # sanity checker
        if (percentage < 0):
            percentage = 0
        elif (percentage > 100):
            percentage = 100
        multiplier = 655.35
        duty_cycle = int(float(percentage) * multiplier)
        return duty_cycle


    # One channel off and the another at given speed
    def forward(self, speed_percent = 100) -> None:
        # first turn off backwards
        self.__pin_backward_pwm.duty_u16(0)
        # enable forward
        duty_cycle = self.percent_to_rp_duty(speed_percent)
        self.__pin_forward_pwm.duty_u16(duty_cycle)
        

    # One channel off and the another at given speed
    def backward(self, speed_percent = 100) -> None:
        # first turn off forward
        self.__pin_forward_pwm.duty_u16(0)
        # enable forward
        duty_cycle = self.percent_to_rp_duty(speed_percent)
        self.__pin_backward_pwm.duty_u16(duty_cycle)
        
    # Stop motor
    def stop_instant(self) -> None:
        self.__pin_backward_pwm.duty_u16(0)
        self.__pin_forward_pwm.duty_u16(0)


# setup motor control pins and initialize class
motor = SN754410NE_motor(backward_pin=16, forward_pin=17)

# while True:
#     motor.forward(35)
#     time.sleep_ms(3000)
#     motor.stop_instant()
#     time.sleep_ms(500)
#     motor.backward(35)
#     time.sleep_ms(3000)
#     motor.stop_instant()
#     time.sleep_ms(500)
    
# # For the tests
# while True:
#     for duty_p in range(0,100):
#         duty = percent_to_rp_duty(duty_p)
#         print(duty)
#         pin_backward_pwm.duty_u16(duty)
#         time.sleep_ms(10)
#         
#     for duty_p in range(100,0, -1):
#         duty = percent_to_rp_duty(duty_p)
#         print(duty)
#         pin_backward_pwm.duty_u16(duty)
#         time.sleep_ms(10)