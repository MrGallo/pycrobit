import abc
import threading
import time

from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import List

import serial

import pycrobit.utils as utils


class ConnectionError(Exception):
    pass


class Microbit:
    def __init__(self):
        self._data = None
        self._serial_connection = serial.Serial()
        self.accelerometer = Accelerometer()
        self.button_a = Button()
        self.button_b = Button()
        self.__read_data = True

    def connect(self, port=None, baud=115200, stopbits=1, fetch_delay=0.01):
        self._serial_connection.port = port
        self._serial_connection.baudrate = baud
        self._serial_connection.stopbits = stopbits
        try:
            self._serial_connection.open()
        except serial.serialutil.SerialException:
            raise ConnectionError("Cannot connect to the Micro:bit. "
                                  "Ensure it is plugged in and you are using "
                                  "the correct port name.")

        self.__t = threading.Thread(target=self._read_data(fetch_delay))
        self.__t.start()

    def disconnect(self):
        self.__read_data = False
        self.__t.join()

    def is_connected(self):
        return self._serial_connection.is_open

    def _read_data(self, delay=0.01):
        def func():
            while self.__read_data:
                try:
                    data_string = self._serial_connection.readline().decode("utf-8").strip()
                    self._data = utils.string_to_object(data_string)
                    self._sort_data()
                except UnicodeDecodeError:
                    "Read from microbit failed"
                    # print("failed")
                except utils.JSONStringCorruptError:
                    "Read worked, data string corrupt."
                    print(f"CORRUPT: {data_string}")
                time.sleep(delay)
            self._serial_connection.close()
        return func

    def _sort_data(self):
        self.accelerometer._x = self._data.x
        self.accelerometer._y = self._data.y
        self.accelerometer._z = self._data.z

        self.accelerometer._gestures = self._data.get_gestures
        self.accelerometer._current_gesture = self._data.current_gesture

        # Buttons
        self.button_a._is_pressed = self._data.button_a_is_pressed
        self.button_b._is_pressed = self._data.button_b_is_pressed

        self.button_a._was_pressed = self._data.button_a_was_pressed
        self.button_b._was_pressed = self._data.button_b_was_pressed

        self.button_a._presses = self._data.button_a_get_presses
        self.button_b._presses = self._data.button_b_get_presses


class Accelerometer:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._z = 0
        self._gestures = []
        self._current_gesture = ""

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def get_values(self):
        return self._x, self._y, self._z

    def get_gestures(self):
        return self._gestures

    def current_gesture(self):
        return self._current_gesture

    def is_gesture(self, name):
        return self._current_gesture == name


@dataclass
class Button:
    _is_pressed: bool=False
    _presses: int=0
    _was_pressed: bool=False

    def press(self):
        self._is_pressed = True
    
    def release(self):
        self._is_pressed = False

    def is_pressed(self):
        return self._is_pressed
    
    def was_pressed(self):
        was_pressed = self._was_pressed
        self._was_pressed = False  # ensure True for only one frame
        return was_pressed
    
    def get_presses(self):
        return self._presses


@contextmanager
def connect_microbit(port=None, baud=115200, stopbits=1, fetch_delay=0.01):
    mb = Microbit()
    mb.connect(port=port, baud=baud, stopbits=stopbits, fetch_delay=fetch_delay)
    yield mb
    mb.disconnect()
