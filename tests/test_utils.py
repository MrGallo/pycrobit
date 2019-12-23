from itertools import count

import pytest

from pycrobit.utils import *


def test_string_to_dict():
    assert string_to_dict('{"one": 1, "two": "two"}')['one'] == 1
    assert string_to_dict('{"one": 1, "two": "two"}')['two'] == "two"
    with pytest.raises(JSONStringCorruptError):
        assert string_to_dict('{"one: 1, "two": "two"}')


def test_dict_to_object():
    d = {}
    d['x'] = 1
    d['y'] = 3
    d['z'] = 5

    assert dict_to_object(d).x == 1
    assert dict_to_object(d).y == 3


def test_string_to_object():
    data = string_to_object('{"one": 1, "two": "two", "three": false}')
    assert data.one == 1
    assert data.two == "two"
    assert data.three is False


def test_map_value():
    assert map_value(10, 0, 10, 0, 100) == 100
    assert map_value(5, 0, 10, 0, 100) == 50
    assert map_value(0, -1, 1, 0, 100) == 50
    assert map_value(0, -1, 1, 50, 60) == 55
    assert map_value(10, -20, 20, 0, 100) == 75
    assert map_value(0, -20, 20, -5, 5) == 0


def test_dict_to_string():
    keys = list("abcd")
    data = dict(zip(keys, count(5)))
    assert dict_to_string(data) == '{"a": 5, "b": 6, "c": 7, "d": 8}'
    
    # can encode Python bool to JSON bool
    data = {}
    data['one'] = False
    assert dict_to_string(data) == '{"one": false}'
    data['one'] = True
    assert dict_to_string(data) == '{"one": true}'
