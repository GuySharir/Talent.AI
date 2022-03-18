from enum import Enum


class ListDistMethod(Enum):
    intersection = 1
    inner_product = 2
    freq_order_lists = 3


class NestedDistMethod(Enum):
    all_items = 1
    only_correlate_attributes = 2
    all_items_when_correlate_attributes = 3
