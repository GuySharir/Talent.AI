import math
from pydoc import locate


def my_print(*args):
    pass


class DistanceCateFunctions:
    """
        This class (DistanceFunctions) contains all categorical distance calculation equations based on
        "An incremental mixed data clustering method using a new distance measure"
        article. (published on 6 may 2014)
        - self.domain_size, domain size of a given attribute (the number of possible values for the given attribute)
        - self.value_frequency, the frequency of a possible value in the given attribute

        - self.domain_per_attribute, for each attribute in the data represent its domain size
            (the number of possible values)

        - self.freq_per_attribute, for each attributes' value in the data represent its frequency

        - self.attr_types, represent attributes types
            {name: <str>, experience: dict, ..}

        - self.nested_attr_types, represent nested attributes types
            {experience:{company_name: <str>, company_size: <float>, ...}}

        - self.sum, represents the total categorical distance

        - q2, calculate the categorical distance of two attribute values regarding the domain size that is obtained
         heuristically.
            * domain_size_z - represent the domain size for an attribute

        - q3, calculate the distance of two value attribute (k) regarding their occurrence frequencies
            in a given attribute k
            * val1_frequency - represent the frequency of a value1 in  attribute k
            * val2_frequency - represent the frequency of a value2 in  attribute k

        - q10, calculates the distance of two values of attribute k in the data set, exploiting unsupervised
         information (in our case)

        - q11,
        - q12,
        - calc_num_distance_q13,
        - q14,
    """

    def __init__(self, instance_a: object, instance_b: object,
                 attr_type: dict, nested_attr_types: dict, freq_per_attribute: dict, domain_per_attribute: dict):
        self.attr_types = attr_type
        self.nested_attr_types = nested_attr_types
        self.domain_per_attribute = domain_per_attribute
        self.freq_per_attribute = freq_per_attribute

        self.instance_a = {attr: instance_a[inx] for inx, attr in enumerate(self.attr_types.keys())}
        self.instance_b = {attr: instance_b[inx] for inx, attr in enumerate(self.attr_types.keys())}

        self.categorical_sum = 0
        self.numerical_sum = 0

    def q2(self, domain_size) -> float:
        if domain_size >= 3:
            return 1
        elif 3 < domain_size <= 10:
            return 1 - (0.05 * (domain_size - 3))
        elif domain_size > 10:
            return 0.65 - (0.01 * (domain_size - 10))

    def q3(self, val1, val2, value_frequency: dict) -> float:
        if not val1:
            val1 = 'null'
        if not val2:
            val2 = 'null'

        min_freq = min(value_frequency.items(), key=lambda x: x[1])[1]
        my_print(f'min frequency {min_freq}')
        val1_frequency = value_frequency.get(val1)
        val2_frequency = value_frequency.get(val2)
        print(f'v1 freq {val1_frequency} v2 freq {val2_frequency}')
        max_freq = max(val1_frequency, val2_frequency)
        dist = (abs(val1_frequency - val2_frequency) + min_freq) / max_freq

        # my_print(f'distance per frequency {dist}')
        return dist

    def q10(self, val1, val2, value_frequency: dict, domain_size):
        my_print(f'equation q2 return value - {self.q2(domain_size=domain_size)}')
        my_print(f'equation q3 return value - {self.q3(val1=val1, val2=val2, value_frequency=value_frequency)}')
        q3result = self.q3(val1=val1, val2=val2, value_frequency=value_frequency)
        q2result = self.q2(domain_size=domain_size)

        if not q3result and not q2result:
            return 0
        elif not q3result and q2result:
            return q2result
        elif q3result and not q2result:
            return q3result
        else:
            return max(q3result, q2result)

    def q12(self, attribute):
        if self.instance_a[attribute] == self.instance_b[attribute]:
            return 0
        elif self.instance_a[attribute] != self.instance_b[attribute]:
            return 1

    @staticmethod
    def calc_num_distance_q13(val1, val2) -> float:
        my_print(f'numeric {val1} , {val2}')
        if not val1 or not val2:
            return 0
        else:
            return (val1 - val2) ** 2

    @staticmethod
    def dist_for_lists(list1, list2) -> float:
        union = list(set(list1 + list2))
        intersection = list(set.intersection(set(list1), set(list2)))

        union_len = len(union)
        intersection_len = len(intersection)
        my_print(f'list1 {list1}\nlist2 {list2}')
        my_print(f'union {union}\ninter {intersection}\nunion len {union_len}\ninter len {intersection_len}')

        if union_len == 0:
            return 0

        return intersection_len / union_len

    def q11(self):
        for attr, val in self.instance_a.items():
            val_type = locate(self.attr_types[attr].split("'")[1])

            if val_type == str:
                my_print("####################################################################################")
                my_print(val_type)
                my_print(f'attr {attr}')
                my_print(self.domain_per_attribute[attr])
                my_print(f'instance a value - {val}\ninstance b value - {self.instance_b[attr]}')
                my_print(f'the attribute value freq dictionary {self.freq_per_attribute[attr]}')
                q10result = self.q10(val, self.instance_b[attr], self.freq_per_attribute[attr],
                                     self.domain_per_attribute[attr])
                q12result = self.q12(attr)

                my_print(f'q10 result {q10result}\nq12 result {q12result}')
                self.categorical_sum += (q10result * q12result)

            elif val_type == float or val_type == int:
                q13result = self.calc_num_distance_q13(val, self.instance_b[attr])
                my_print("####################################################################################")
                my_print(val_type)
                my_print(f'q13 result {q13result}\n')
                self.numerical_sum += q13result

            elif val_type == list:
                list_dist_result = self.dist_for_lists(val, self.instance_b[attr])
                self.categorical_sum += list_dist_result
                my_print("####################################################################################")
                my_print(val_type)
                my_print(f'list dist result {list_dist_result}\n')

            elif val_type == dict:
                pass

        my_print(f'categorical sum result {self.categorical_sum}')
        my_print(f'numerical sum result {self.numerical_sum}')

    def q14(self):
        return math.sqrt(self.categorical_sum + self.numerical_sum)

    def calc_distance(self):

        my_print(f'attr types {self.attr_types}')
        my_print(f'nested attr types {self.nested_attr_types}')
        # my_print(f'freq per attr {self.freq_per_attribute}')
        # my_print(f'domain per attr {self.domain_per_attribute}')
        #
        # self.instance_a = {attr: self.instance_a[inx] for inx, attr in enumerate(self.attr_types.keys())}
        # self.instance_b = {attr: self.instance_b[inx] for inx, attr in enumerate(self.attr_types.keys())}
        my_print(f'instance a - {self.instance_a}')
        my_print(f'instance b - {self.instance_b}')

        self.q11()
        # my_print(f'total distance result {self.q14()}')
        return self.q14()


if __name__ == '__main__':
    interest = {'web applications': 2, 'web development': 4,
                'programming': 3, 'entrepreneurship': 3}

    dist_value = DistanceCateFunctions(interest, 12).q10('web development', 'programming')
    my_print(f'dist return value - {dist_value}')
