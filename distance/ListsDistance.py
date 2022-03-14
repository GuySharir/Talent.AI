from distance.DistEnum import ListDistMethod
from distance.DistanceData import ListDistanceData


class ListsDistance:
    def __init__(self, list_distance_data: ListDistanceData):
        self.list_distance_data = list_distance_data

    def calc_dist(self) -> float:
        if self.list_distance_data.lists_dist_method == ListDistMethod.intersection:
            return self.intersection()
        elif self.list_distance_data.lists_dist_method == ListDistMethod.inner_product:
            return self.inner_product()

    def intersection(self) -> float:
        union = list(set(self.list_distance_data.list1 + self.list_distance_data.list2))
        intersection = list(set.intersection(set(self.list_distance_data.list1), set(self.list_distance_data.list2)))

        union_len = len(union)
        intersection_len = len(intersection)
        print(f'list1 {self.list_distance_data.list1}\nlist2 {self.list_distance_data.list2}')
        print(f'union {union}\ninter {intersection}\nunion len {union_len}\ninter len {intersection_len}')

        if union_len == 0:
            return 0

        return intersection_len / union_len

    def inner_product(self) -> float:
        pass
