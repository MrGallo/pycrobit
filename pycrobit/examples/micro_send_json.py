"""
Microbit: Send JSON
Load this on a Microbit to send JSON data over a serial connection.
"""

from microbit import *


def dict_to_string(data):
    """Takes a dictionary and converts it to a string to send
    over serial connection with Micro:Bit

    Args:
        data: Dict
    Returns:
        str: JSON string of the data.
    """
    return (str(data).replace("'", '"')
                     .replace(": False", ": false")
                     .replace(": True", ": true"))


while True:
    data = {}

    # Accelerometer
    x, y, z = accelerometer.get_values()
    data['x'] = x
    data['y'] = y
    data['z'] = z

    # Gestures
    data['get_gestures'] = list(accelerometer.get_gestures())
    data['current_gesture'] = accelerometer.current_gesture()

    # Buttons
    data['button_a_is_pressed'] = button_a.is_pressed()
    data['button_b_is_pressed'] = button_b.is_pressed()

    data['button_a_was_pressed'] = button_a.was_pressed()
    data['button_b_was_pressed'] = button_b.was_pressed()

    data['button_a_get_presses'] = button_a.get_presses()
    data['button_b_get_presses'] = button_b.get_presses()

    print(dict_to_string(data))
    sleep(10)
