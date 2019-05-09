from typing import Dict
from itertools import count

from bit_utils import *


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
