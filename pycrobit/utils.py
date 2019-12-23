import json

from collections import namedtuple

from typing import Dict, NamedTuple


class JSONStringCorruptError(Exception):
    pass


def string_to_dict(string: str) -> Dict:
    try:
        return json.loads(string)
    except json.decoder.JSONDecodeError:
        raise JSONStringCorruptError(f"Cannot decode string: {string}")


def dict_to_object(data_dict: Dict) -> NamedTuple:
    """Converts dict to an object"""
    try:
        Data = namedtuple("Data", " ".join(data_dict.keys()))
    except AttributeError:
        raise TypeError("Must be a dict.")
    data = Data(**data_dict)
    return data


def string_to_object(data_string: str) -> NamedTuple:
    return dict_to_object(string_to_dict(data_string))


def map_value(value: float,
              min_a: float,
              max_a: float,
              min_b: float,
              max_b: float) -> float:
    return min_b + (value - (min_a))/(max_a - (min_a)) * (max_b - min_b)


# Functions to be flashed to the Microbit

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