class CateDistance:
    """
        This class (CateDistance) calculate distance between two values
        of categorical attributes
        - self.numeric_attr_dist, is the return value. A dictionary contains the attribute name and
        the distance result
        {experience: val}
        - val_a, val_b, contains categorical value
        - attr, refers to the current attribute name
        """
    def __init__(self, attribute: str, val_a, val_b):
        self.cate_attr_dist = {}
        self.val_a = val_a
        self.val_b = val_b
        self.attr = attribute

    def calc_str_distance(self, attribute: str) -> float:
        pass

    def calc_list_attributes(self):
        pass

    def calc_nested_attributes(self):
        pass


if __name__ == '__main__':
    pass
    # CateDistance(value_a, value_b)
