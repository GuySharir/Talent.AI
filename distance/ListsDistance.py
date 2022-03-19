from distance.DistEnum import ListDistMethod
from distance.DistanceData import ListDistanceData
from distance.DistanceFunctions import DistanceNumStr
from dataTool.runtimeObjectsInfo.ListLengthData import LIST_LENGTH_PER_ATTR


class ListsDistance:
    def __init__(self, list_distance_data: ListDistanceData):
        self.list_distance_data = list_distance_data

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

    @staticmethod
    def prepare_list_to_dist(length: int, list_length_expected: int, list_obj: list) -> list:
        if length < list_length_expected:
            while len(list_obj) < list_length_expected:
                list_obj.append('$')
        elif length > list_length_expected:
            list_obj = list_obj[:list_length_expected]

        return list_obj

    def order_list_by_freq(self, list_obj: list) -> list:
        # order list by freq for attr
        return list_obj

    def freq_list_all(self, ordered: bool = False) -> float:
        dist_obj = DistanceNumStr()
        list_dist_calc_result = []
        list_length_expected = LIST_LENGTH_PER_ATTR[self.list_distance_data.attribute]
        self.list_distance_data.value_frequency['$'] = 0

        len_list1 = len(self.list_distance_data.list1)
        len_list2 = len(self.list_distance_data.list2)

        list1 = self.prepare_list_to_dist(length=len_list1, list_length_expected=list_length_expected,
                                          list_obj=self.list_distance_data.list1)
        list2 = self.prepare_list_to_dist(length=len_list2, list_length_expected=list_length_expected,
                                          list_obj=self.list_distance_data.list2)

        # for range in length send elements to str distance calculation and sum to categorical val
        if ordered:
            list1 = self.order_list_by_freq(list_obj=list1)
            list2 = self.order_list_by_freq(list_obj=list2)
            for i in range(list_length_expected):
                result = dist_obj.distance_per_type(val_type=str, val1=list1[i], val2=list2[i],
                                                    value_frequency=self.list_distance_data.value_frequency,
                                                    domain_size=self.list_distance_data.domain_size,
                                                    attribute=self.list_distance_data.attribute,
                                                    instance_a={self.list_distance_data.attribute: list1},
                                                    instance_b={self.list_distance_data.attribute: list2})
                list_dist_calc_result.append(result)
        else:
            # for loop in for loop nxn
            pass
        print()

        return 0

    def calc_dist(self) -> float:
        if self.list_distance_data.lists_dist_method == ListDistMethod.intersection:
            return self.intersection()
        elif self.list_distance_data.lists_dist_method == ListDistMethod.inner_product:
            return self.inner_product()
        elif self.list_distance_data.lists_dist_method == ListDistMethod.freq_order_lists:
            return self.freq_list_all(ordered=True)
        elif self.list_distance_data.lists_dist_method == ListDistMethod.freq_list_all:
            return self.freq_list_all()
