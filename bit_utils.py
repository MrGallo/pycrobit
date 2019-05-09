"""
Microbit Utils
Copy and paste these functions to use within your Microbit code.
"""


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
