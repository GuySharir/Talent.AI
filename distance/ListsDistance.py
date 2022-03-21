from distance.DistEnum import ListDistMethod
from distance.DistanceData import ListDistanceData
from distance.DistanceFunctions import DistanceNumStr
from dataTool.runtimeObjectsInfo.ListLengthData import LIST_LENGTH_PER_ATTR


def my_print(message):
    pass


class ListsDistance:
    def __init__(self, list_distance_data: ListDistanceData):
        self.list_distance_data = list_distance_data

    def intersection(self) -> float:
        union = list(set(self.list_distance_data.list1 + self.list_distance_data.list2))
        intersection = list(set.intersection(set(self.list_distance_data.list1), set(self.list_distance_data.list2)))

        union_len = len(union)
        intersection_len = len(intersection)
        my_print(f'list1 {self.list_distance_data.list1}\nlist2 {self.list_distance_data.list2}')
        my_print(f'union {union}\ninter {intersection}\nunion len {union_len}\ninter len {intersection_len}')

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

    def descending_freq_order(self) -> list:
        sorted_freq = sorted(self.list_distance_data.value_frequency.items(), key=lambda x: x[1], reverse=True)
        sorted_freq_values = [i[0] for i in sorted_freq]
        print(f'sorted freq in descending order- {sorted_freq_values}')

        return sorted_freq_values

    @staticmethod
    def order_list_by_freq(list_obj: list, sorted_freq_values: list) -> list:
        sorted_freq_in_list_obj = [x for x in sorted_freq_values if x in list_obj]
        result_list = sorted(list_obj, key=lambda ele: sorted_freq_in_list_obj.index(ele))
        return result_list

    def freq_list_all(self, ordered: bool = False) -> float:
        dist_obj = DistanceNumStr()
        list_dist_calc_result = []
        list_length_expected = LIST_LENGTH_PER_ATTR[self.list_distance_data.attribute]
        print(f'list length expected: {list_length_expected} ')
        self.list_distance_data.value_frequency['$'] = 1

        len_list1 = len(self.list_distance_data.list1)
        len_list2 = len(self.list_distance_data.list2)

        list1 = self.prepare_list_to_dist(length=len_list1, list_length_expected=list_length_expected,
                                          list_obj=self.list_distance_data.list1)
        list2 = self.prepare_list_to_dist(length=len_list2, list_length_expected=list_length_expected,
                                          list_obj=self.list_distance_data.list2)
        print(f'lists after length preparation- 1: {list1}\n2: {list2} ')

        # for range in length send elements to str distance calculation and sum to categorical val
        if ordered:
            sorted_freq_values = self.descending_freq_order()
            list1 = self.order_list_by_freq(list_obj=list1, sorted_freq_values=sorted_freq_values)
            list2 = self.order_list_by_freq(list_obj=list2, sorted_freq_values=sorted_freq_values)
            print(f'ordered lists- 1: {list1}\n2: {list2} ')
            for i in range(list_length_expected):
                result = dist_obj.distance_per_type(val_type=str, val1=list1[i], val2=list2[i],
                                                    value_frequency=self.list_distance_data.value_frequency,
                                                    domain_size=self.list_distance_data.domain_size,
                                                    attribute=self.list_distance_data.attribute,
                                                    instance_a={self.list_distance_data.attribute: list1},
                                                    instance_b={self.list_distance_data.attribute: list2})
                list_dist_calc_result.append(result)
            print(f'list_dist_calc_result: {list_dist_calc_result}')
            return sum(list_dist_calc_result)
        else:
            for val1 in list1:
                for val2 in list2:
                    result = dist_obj.distance_per_type(val_type=str, val1=val1, val2=val2,
                                                        value_frequency=self.list_distance_data.value_frequency,
                                                        domain_size=self.list_distance_data.domain_size,
                                                        attribute=self.list_distance_data.attribute,
                                                        instance_a={self.list_distance_data.attribute: list1},
                                                        instance_b={self.list_distance_data.attribute: list2})
                    list_dist_calc_result.append(result)
            print(f'list_dist_calc_result: {list_dist_calc_result}')
            return sum(list_dist_calc_result)

    def calc_dist(self) -> float:
        print(f'list attribute- {self.list_distance_data.attribute}')
        print(f'given lists- 1: {self.list_distance_data.list1}\n2: {self.list_distance_data.list2} ')
        if self.list_distance_data.lists_dist_method == ListDistMethod.intersection:
            return self.intersection()
        elif self.list_distance_data.lists_dist_method == ListDistMethod.inner_product:
            return self.inner_product()
        elif self.list_distance_data.lists_dist_method == ListDistMethod.freq_order_lists:
            return self.freq_list_all(ordered=True)
        elif self.list_distance_data.lists_dist_method == ListDistMethod.freq_list_all:
            return self.freq_list_all()
