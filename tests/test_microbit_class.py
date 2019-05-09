import time

from dataclasses import dataclass
from itertools import cycle

from pycrobit import Microbit, Accelerometer


@dataclass
class FakeSerial:
    port: str=None
    baud: int=115200
    stopbits: int=1
    _is_open: bool=False

    def __post_init__(self):
        self._lines = iter((
            b'{"x": 1, "y": 3, "z": 5}\n',
            b'{"x": 2, "y": 4, "z": 6}\n',
            b'{"x": 3, "y": 5, "z": 7}\n',
        ))

    def open(self):
        self._is_open = True

    def close(self):
        self._is_open = False

    @property
    def is_open(self):
        return self._is_open
    
    def readline(self):
        return next(self._lines)


def test_can_connect_to_microbit():
    mb = Microbit()
    mb._serial_connection = FakeSerial()
    mb.connect(port="COM3", baud=115200, stopbits=1)
    assert mb.is_connected() is True, "Should be connected"

    mb.disconnect()
    assert mb.is_connected() is False

    mb2 = Microbit()
    assert mb2.is_connected() is False


def test_get_json_from_microbit():
    mb = Microbit()
    mb._serial_connection = FakeSerial()
    mb.connect("COM3", fetch_delay=0.01)
    time.sleep(0.2)
    assert mb.accelerometer.get_x() != 0
    mb.disconnect()


def test_accelerometer_object():
    microbit = Microbit()
    assert isinstance(microbit.accelerometer, Accelerometer)
    accel = Accelerometer()
    microbit.accelerometer = accel
    accel._x = 1
    accel._y = 3
    accel._z = 5

    assert microbit.accelerometer.get_x() == 1
    assert microbit.accelerometer.get_y() == 3
    assert microbit.accelerometer.get_z() == 5
    assert microbit.accelerometer.get_values() == (1, 3, 5)


def test_button_a():
    microbit = Microbit()
    assert microbit.button_a.is_pressed() is False

    microbit.button_a.press()
    assert microbit.button_a.is_pressed() is True
    
    microbit.button_a.release()
    assert microbit.button_a.is_pressed() is False

"""
# connect to microbit
# get and convert data
# access microbit properties according to api
    - accelerometer
        - get_x() (y and z)
    - 
"""