from distance.DistEnum import ListDistMethod


class ListsDistance:
    def __init__(self, list1: list, list2: list, freq_per_attribute: dict, lists_dist_method: ListDistMethod):
        self.freq_per_attribute = freq_per_attribute
        self.lists_dist_method = lists_dist_method
        self.list1 = list1
        self.list2 = list2

    def calc_dist(self) -> float:
        if self.lists_dist_method == ListDistMethod.intersection:
            return self.intersection()
        elif self.lists_dist_method == ListDistMethod.inner_product:
            return self.inner_product()

    def intersection(self) -> float:
        union = list(set(self.list1 + self.list2))
        intersection = list(set.intersection(set(self.list1), set(self.list2)))

        union_len = len(union)
        intersection_len = len(intersection)
        print(f'list1 {self.list1}\nlist2 {self.list2}')
        print(f'union {union}\ninter {intersection}\nunion len {union_len}\ninter len {intersection_len}')

        if union_len == 0:
            return 0

        return intersection_len / union_len

    def inner_product(self) -> float:
        pass
