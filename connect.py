from umqtt.simple import MQTTClient
from time import sleep
from machine import Pin, PWM
import ubinascii
import micropython
import machine

led = Pin(12, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)
servo = PWM(Pin(15), Pin.OUT, freq=100, Duty=77)

SERVER = "192.168.0.35"
C_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"lock"

state = 0



def led_toggle():
    led.value(not led.value())
    pass


def sub(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(1)
        servo.duty(35)
        state = 1
    elif msg == b"off":
        led.value(0)
        servo.duty(122)
        state = 0
    elif msg == b"toggle":
        led.value(state)
        state = 1 - state


def main(server=SERVER):
    while True:
        if not button.value():
            led_toggle()
            sleep(0.5)
        pass
    c = MQTTClient(C_ID, server)
    c.set_callback(sub)
    c.connect()
    c.subscribe(TOPIC)
    print("connect to %s, topic is %s," % (TOPIC, server))

    try:
        while 1:
            # micropython.mem_info()
            c.wait_msg()
    finally:
        c.disconnect()

    if __name__ == '__main__':
        main()
