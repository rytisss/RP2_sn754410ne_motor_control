from machine import Pin, PWM
from rotary_irq_rp2 import RotaryIRQ
from sn754410ne_motor_control import SN754410NE_motor
import time


if __name__ == "__main__":
    # setup motor control pins and initialize class
    motor = SN754410NE_motor(backward_pin=16, forward_pin=17)
    motor.stop_instant()
    motor.forward(35)
    
    # setup encoder
    encoder = RotaryIRQ(19, 20, pull_up=False)
    current_val = -1  # Track the last known value of the encoder
    while True:
        new_val = encoder.value()  # What is the encoder value right now?
        if current_val != new_val:  # The encoder value has changed!
            print('Encoder value:', new_val)  # Do something with the new value
            current_val = new_val  # Track this change as the last know value
#     while True:
#         motor.forward(35)
#         time.sleep_ms(3000)
#         motor.stop_instant()
#         time.sleep_ms(500)
#         motor.backward(35)
#         time.sleep_ms(3000)
#         motor.stop_instant()
#         time.sleep_ms(500)
