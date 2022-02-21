class NumDistance:
    """
    This class (NumDistance) calculate distance between two values
    of a single numerical attribute
    - self.numeric_attr_dist, is the return value. A dictionary contains the attribute name and
    the distance result
    {age: val}
    - val_a, val_b, contains categorical value
    - attr, refers to the current attribute name
    """
    def __init__(self, attribute: str, val_a, val_b):
        self.numeric_attr_dist = {}
        self.val_a = val_a
        self.val_b = val_b
        self.attr = attribute

    def calc_num_distance(self) -> dict:
        if not self.val_a or not self.val_b:
            return {self.attr: 0}
        else:
            return {self.attr: (self.val_a - self.val_b) ** 2}


if __name__ == '__main__':
    pass
