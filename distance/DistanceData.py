from dataclasses import dataclass
from distance.DistEnum import ListDistMethod


@dataclass
class ListDistanceData:
    val_type: object
    list1: list
    list2: list
    value_frequency: dict
    domain_size: int
    attribute: str
    lists_dist_method: ListDistMethod


@dataclass
class NumDistanceData:
    val_type: object
    val1: float
    val2: float
    value_frequency: dict
    domain_size: int
    attribute: str


@dataclass
class StrDistanceData:
    val_type: object
    val1: str
    val2: str
    value_frequency: dict
    domain_size: int
    attribute: str
    instance_a: dict
    instance_b: dict

