"""Klassen for keypad"""
import time
import RPi.GPIO as GPIO


class Keypad():
    """Tolker input fra tastaturet"""

    def __init__(self):
        self.setup()

    def setup(self):
        """Setter opp input- og output pins"""
        GPIO.setmode(GPIO.BCM)

        # row pins
        GPIO.setup(18, GPIO.OUT)  # R0
        GPIO.setup(23, GPIO.OUT)  # R1
        GPIO.setup(24, GPIO.OUT)  # R2
        GPIO.setup(25, GPIO.OUT)  # R3

        # column pins
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # C0
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # C1
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # C2

    def do_polling(self):
        """Sjekker for knappetrykk"""
        GPIO.setmode(GPIO.BCM)

        symbol_pairs = {(18, 17): 1, (18, 27): 2, (18, 22): 3,
                        (23, 17): 4, (23, 27): 5, (23, 22): 6,
                        (24, 17): 7, (24, 27): 8, (24, 22): 9,
                        (25, 17): '*', (25, 27): 0, (25, 22): '#'}

        row_pins = [18, 23, 24, 25]
        column_pins = [17, 27, 22]

        for row_pin in row_pins:  # tar for seg rader en og en
            GPIO.output(row_pin, GPIO.HIGH)

            for column_pin in column_pins:  # tar for seg kolonner

                if GPIO.input(column_pin) == GPIO.HIGH:  # dersom pinen er høy
                    i = 0
                    while i < 20:
                        if GPIO.input(
                                column_pin) == GPIO.HIGH:  # teller opp 20 ganger at pinen er høy
                            i += 1
                            time.sleep(0.001)

                    if i == 20:  # dersom i har nådd 20 er pinen høy
                        GPIO.output(row_pin, GPIO.LOW)
                        return str(symbol_pairs.get((row_pin, column_pin)))

            GPIO.output(row_pin, GPIO.LOW)
        return None

    def get_next_signal(self):
        """Utfører polling frem til et tastetrykk detekteres"""
        next_signal = None

        while next_signal is None:
            next_signal = self.do_polling()

        return next_signal
