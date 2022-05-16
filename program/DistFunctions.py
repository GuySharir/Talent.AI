import math
from dataclasses import dataclass
from program.ReadData import read_freq_per_value_data, read_domain_per_attr_data, DATA_TYPE_PER_INDEX, \
    ATTRIBUTE_PER_INDEX
from dataTool.runtimeObjectsInfo.ListLengthData import LIST_LENGTH_PER_ATTR, NESTED_LENGTH_PER_ATTR


@dataclass
class DistanceData:
    instance1: list
    instance2: list
    val1_frequency: float
    val2_frequency: float
    frequency: dict
    domain_size: int
    attribute_inx: int


class DistanceFunctions:
    def __init__(self, data: DistanceData):
        self.data = data

    def q2(self) -> float:
        if self.data.domain_size <= 3:
            return 1
        elif 3 < self.data.domain_size <= 10:
            return 1 - (0.05 * (self.data.domain_size - 3))
        elif self.data.domain_size > 10:
            return 0.65 - (0.01 * (self.data.domain_size - 10))

    def q3(self) -> float:
        min_freq = min(self.data.frequency.items(), key=lambda x: x[1])[1]
        max_freq = max(self.data.val1_frequency, self.data.val2_frequency)
        dist = (abs(self.data.val1_frequency - self.data.val2_frequency) + min_freq) / max_freq
        return dist

    def q10(self) -> float:
        q3result = self.q3()
        q2result = self.q2()

        if not q3result and not q2result:
            return 0
        elif not q3result and q2result:
            return q2result
        elif q3result and not q2result:
            return q3result
        else:
            return max(q3result, q2result)

    def q12(self) -> float:
        if self.data.instance1[self.data.attribute_inx] == self.data.instance2[self.data.attribute_inx]:
            return 0
        elif self.data.instance1[self.data.attribute_inx] != self.data.instance2[self.data.attribute_inx]:
            return 1


def calc_num_distance_q13(val1, val2) -> float:
    # change missing value according to michal article
    # if not val1 or not val2:
    #     return 0
    # else:
    return (val1 - val2) ** 2


def categorical_dist_between_freq_vectors(attr_type, data: DistanceData = None) -> float:
    if attr_type == str or attr_type == bool:
        data = data
        str_obj = DistanceFunctions(data=data)
        q10result = str_obj.q10()
        q12result = str_obj.q12()
        return (q10result * q12result) ** 2


def numerical_dist_between_freq_vectors(attr_type, num_val1=None, num_val2=None):
    if attr_type == int or attr_type == float:
        q13result = calc_num_distance_q13(val1=num_val1, val2=num_val2)
        return q13result


def q14(categorical_sum, numerical_sum) -> float:
    return math.sqrt(categorical_sum + numerical_sum)


def prepare_data_for_dist_calc_between_freq_vectors(vec1: list, vec2: list):
    cat_distance_result = []
    num_distance_result = []

    domain = read_domain_per_attr_data()
    freq = read_freq_per_value_data()

    for inx, val in enumerate(vec1):
        attr = ATTRIBUTE_PER_INDEX[inx]
        attr_freq = freq[attr]
        attr_domain = domain[attr]

        if DATA_TYPE_PER_INDEX[inx] == str:
            data = DistanceData(instance1=vec1, instance2=vec2, val1_frequency=val,
                                val2_frequency=vec2[inx], frequency=attr_freq,
                                domain_size=attr_domain, attribute_inx=inx)

            cat_distance_result.append(categorical_dist_between_freq_vectors(attr_type=DATA_TYPE_PER_INDEX[inx],
                                                                             data=data))

        elif DATA_TYPE_PER_INDEX[inx] == float or DATA_TYPE_PER_INDEX[inx] == int:
            num_distance_result.append(numerical_dist_between_freq_vectors(attr_type=DATA_TYPE_PER_INDEX[inx],
                                                                           num_val1=val, num_val2=vec2[inx]))

    # print(f'categorical result-\n {cat_distance_result}')
    # print(f'numerical result-\n {num_distance_result}')
    distance_result = q14(categorical_sum=sum(cat_distance_result), numerical_sum=sum(num_distance_result))
    # print(f'distance result-\n {distance_result}')
    return distance_result


if __name__ == '__main__':
    instance1_ = {'laura gao': [1, 3, 1, 144, 1996.0, 462, 69, 1, 107, 101, 61, 61, 16]}
    instance2_ = {'bruk argaw': [1, 1, 1, 775, 1991.0, 1, 69, 145, 668, 544, 61, 61, 15]}

    vec1_ = [1, 3, 1, 144, 1996.0, 462, 69, 1, 107, 101, 61, 61, 16]
    vec2_ = [1, 1, 1, 775, 1991.0, 1, 69, 145, 668, 544, 61, 61, 15]
    prepare_data_for_dist_calc_between_freq_vectors(vec1=vec1_, vec2=vec2_)
