import RPi.GPIO as GPIO
from time import sleep


"""Controlling the charlieplexed LED-board"""
pins = [20, 21, 26]

pin_led_states = [
  [1, 0, -1],  # A
  [0, 1, -1],  # B
  [-1, 1, 0],  # C
  [-1, 0, 1],  # D
  [1, -1, 0],  # E
  [0, -1, 1]   # F
]

GPIO.setmode(GPIO.BCM)


def set_pin(pin_index, pin_state):
    """Sets the required pins to low and high depending on input"""
    if pin_state == -1:
        GPIO.setup(pins[pin_index], GPIO.IN)
    else:
        GPIO.setup(pins[pin_index], GPIO.OUT)
        GPIO.output(pins[pin_index], pin_state)


def light_led(led_number):
    """Lights the leds in pin_led_states"""
    for pin_index, pin_state in enumerate(pin_led_states[led_number]):
        set_pin(pin_index, pin_state)


set_pin(0, -1)
set_pin(1, -1)
set_pin(2, -1)


def twinkle_all_leds(sec):
    """Twinkles the leds"""
    for j in range(sec):
        for i in range(11):
            light_led(i%6)
            sleep(0.1)


def flash_all_leds(sec):
    """All LEDs lights at once"""
    for i in range(sec*160):
        for i in range(6):
            light_led(i)
            sleep(0.001)
    set_pin(0, -1)
    set_pin(1, -1)
    set_pin(2, -1)


def sequence_light(sequence):
    """All the leds light in the sequence by the array"""
    for i in sequence:
        light_led(i)
        sleep(0.5)


def power_up():
    """Power-up sequence"""
    sequence = [3,5,1,2,4,0]
    sequence_light(sequence)


def power_down():
    """Power down sequence"""
    sequence = [0,4,2,1,5,3]
    sequence_light(sequence)

if __name__ == "__main__":
    power_up()
    power_down()

