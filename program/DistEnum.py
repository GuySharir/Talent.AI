from enum import Enum


class DistMethod(Enum):
    intersection = 1
    inner_product = 2
    fix_length_freq = 3
    hamming_distance = 4


class DefaultVal(Enum):
    Nested_default = 1
