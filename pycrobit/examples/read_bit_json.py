import time
import serial

from pycrobit import utils


with serial.Serial('COM3', 115200, stopbits=1) as s:
    while True:
        try:
            data_string = s.readline().decode("utf-8").strip()
            microbit = utils.string_to_object(data_string)
        except UnicodeDecodeError:
            "Read from microbit failed"
            print("failed")
        except utils.JSONStringCorruptError:
            "Read worked, data string corrupt."
            print(f"CORRUPT: {data_string}")
        else:
            pass
            print(microbit)
            # print(f"current_gesture: {microbit.current_gesture}")
            # print(f"get_gestures: {microbit.get_gestures}")
        time.sleep(0.01)
