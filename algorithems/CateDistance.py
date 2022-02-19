class CateDistance:
    def __init__(self, instance_a: dict, instance_b: dict):
        self.cate_attr_dist = {}
        self.instance_a = instance_a
        self.instance_b = instance_b

    def calc_num_distance(self, attribute: str) -> float:
        pass

    def find_numeric_attr(self) -> dict:
        pass


if __name__ == '__main__':
    pass
