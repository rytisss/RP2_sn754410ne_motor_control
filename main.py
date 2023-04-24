import machine
import network
import socket
import time
from picozero import pico_led
from machine import Pin
from rotary_irq_rp2 import RotaryIRQ
from sn754410ne_motor_control import SN754410NE_motor
import time


# wifi credentials
ssid = 'hehehe'
password = 'hehehe'

# global object for editing from every function in the scope
encoder: RotaryIRQ = None
motor: SN754410NE_motor = None
output_pin: Pin = None


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        # blink the LED on the board for a bit
        time.sleep_ms(300)
        pico_led.on()
        time.sleep_ms(300)
        pico_led.off()
    # let LED be on if connected
    pico_led.on()
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(output_state, encoder_pulses):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <p>Motor control</p>
            <form action="./motor_forward">
            <input type="submit" value="Motor Spin Forward" />
            </form>
            <form action="./motor_backward">
            <input type="submit" value="Motor Spin Backward" />
            </form>
            <form action="./stop_motor">
            <input type="submit" value="Stop Motor" />
            </form>
            <p>Encoder Pulses = <b>{encoder_pulses}</b></p>
            <p>Output Control [now - <b>{output_state}</b>]</p>
            <form action="./toggle_output">
            <input type="submit" value="Toggle Output" />
            </form>
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    global motor
    global encoder
    global output_pin
    #Start a web server
    output_state = 'OFF'
    while True:
        # do client connection handling
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/motor_forward?':
            motor.stop_instant()
            time.sleep_ms(500)
            motor.forward(30)
        if request == '/motor_backward?':
            motor.stop_instant()
            time.sleep_ms(500)
            motor.backward(30)
        elif request =='/stop_motor?':
            motor.stop_instant()
        elif request =='/toggle_output?':
            output_pin.toggle()
            output_state = 'ON' if output_pin.value() else 'OFF'
        # read encoder
        encoder_pulses = encoder.value()
        html = webpage(output_state, encoder_pulses)
        client.send(html)
        client.close()


if __name__ == "__main__":
    #global motor
    #global encoder
    #global output_pin
    
    # setup motor control pins and initialize class
    motor = SN754410NE_motor(backward_pin=16, forward_pin=17)
    motor.stop_instant()
    time.sleep_ms(500)
    
    # setup encoder
    encoder = RotaryIRQ(19, 20, pull_up=False)
    
    # configure output pin
    output_pin = Pin(21, mode=Pin.OUT)
    output_pin.off()
    
    try:
        ip = connect()
        connection = open_socket(ip)
        serve(connection)
    except KeyboardInterrupt:
        machine.reset()
