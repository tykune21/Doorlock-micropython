from machine import Pin
from time import sleep

led = Pin(12, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)


def led_toggle():
    led.value(not led.value())
    pass


def main():
    while True:
        if not button.value():
            led_toggle()
            sleep(0.5)
    pass


if __name__ == '__main__':
    main()
