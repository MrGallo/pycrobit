import json

from collections import namedtuple

from typing import Dict


class JSONStringCorruptError(Exception):
    pass


def main():
    pass


def string_to_dict(string: str) -> Dict:
    try:
        return json.loads(string)
    except json.decoder.JSONDecodeError:
        raise JSONStringCorruptError(f"Cannot decode string: {string}")


def dict_to_object(data_dict: Dict):
    """Converts dict to an object"""
    try:
        Data = namedtuple("Data", " ".join(data_dict.keys()))
    except AttributeError:
        raise TypeError("Must be a dict.")
    data = Data(**data_dict)
    return data


def string_to_object(data_string: str) -> namedtuple:
    return dict_to_object(string_to_dict(data_string))


def map_value(value: float,
              min_a: float,
              max_a: float,
              min_b: float,
              max_b: float) -> float:
    return min_b + (value - (min_a))/(max_a - (min_a)) * (max_b - min_b)


if __name__ == "__main__":
    main()
