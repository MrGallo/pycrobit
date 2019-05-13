# pycrobit
A python library used to communicate with a microbit over a serial connection.

## Usage:

### Flash to Microbit
```python
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
```

### Local Python Script
```python
from pycrobit import Microbit

microbit = Microbit()
microbit.connect(port="COM3")

while not microbit.button_b.is_pressed():
    x, y, z = microbit.accelerometer.get_values()
    print(x, y, z)
    
microbit.disconnect()
```

```python
from pycrobit import connect_microbit

with connect_microbit("COM3") as microbit:
    while not microbit.button_b.is_pressed():
        x, y, z = microbit.accelerometer.get_values()
        print(x, y, z)
```

## Currently Implemented Local API
Accelerometer:
- `microbit.accelerometer.get_x()`
- `microbit.accelerometer.get_y()`
- `microbit.accelerometer.get_z()`
- `microbit.accelerometer.get_values()`
- `microbit.accelerometer.current_gesture()`
- `microbit.accelerometer.is_gesture(name)`

Button A:
- `microbit.button_a.is_pressed()`
- `microbit.button_a.was_pressed()`
- `microbit.button_a.presses()`

Button B
- `microbit.button_b.is_pressed()`
- `microbit.button_b.was_pressed()`
- `microbit.button_b.presses()`


## Checking available COM ports
```python
import serial.tools.list_ports
print([comport.device for comport in serial.tools.list_ports.comports()])
```

## Set permissions in linux
For our computers at school. Check for the appropriate port above.
```sh
$ sudo usermod -a -G dialout USERNAME
$ sudo chmod 666 /dev/ttyACM0
```
