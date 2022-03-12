import math
from pydoc import locate
from distance.ListsDistance import ListsDistance
from distance.NestedDistance import NestedDistance
from distance.DistEnum import ListDistMethod
from distance.DistEnum import NestedDistMethod
from distance.DistanceStrFunctions import DistanceStrFunctions


class DistanceFunctionality:
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
        - q11,
        - q14,
    """

    def __init__(self, instance_a: object, instance_b: object,
                 attr_type: dict, nested_attr_types: dict, freq_per_attribute: dict, domain_per_attribute: dict,
                 lists_dist_method: ListDistMethod, nested_dist_method: NestedDistMethod):
        self.attr_types = attr_type
        self.nested_attr_types = nested_attr_types
        self.domain_per_attribute = domain_per_attribute
        self.freq_per_attribute = freq_per_attribute

        self.instance_a = {attr: instance_a[inx] for inx, attr in enumerate(self.attr_types.keys())}
        self.instance_b = {attr: instance_b[inx] for inx, attr in enumerate(self.attr_types.keys())}

        self.categorical_sum = 0
        self.numerical_sum = 0

        self.lists_dist_method = lists_dist_method
        self.nested_dist_method = nested_dist_method

    def q11(self):
        for attr, val in self.instance_a.items():
            val_type = locate(self.attr_types[attr].split("'")[1])

            if val_type == str:

                print(val_type)
                print(f'attr {attr}')
                print(self.domain_per_attribute[attr])
                print(f'instance a value - {val}\ninstance b value - {self.instance_b[attr]}')
                print(f'the attribute value freq dictionary {self.freq_per_attribute[attr]}')
                q10result = DistanceStrFunctions().q10(val1=val, val2=self.instance_b[attr],
                                                       value_frequency=self.freq_per_attribute[attr],
                                                       domain_size=self.domain_per_attribute[attr])
                q12result = DistanceStrFunctions().q12(attribute=attr, instance_a=self.instance_a,
                                                       instance_b=self.instance_b)

                print(f'q10 result {q10result}\nq12 result {q12result}')
                self.categorical_sum += (q10result * q12result)
                print("####################################################################################")

            elif val_type == float or val_type == int:
                q13result = DistanceStrFunctions().calc_num_distance_q13(val1=val, val2=self.instance_b[attr])

                print(val_type)
                print(f'attr {attr}')
                print(f'q13 result {q13result}\n')
                self.numerical_sum += q13result
                print("####################################################################################")

            elif val_type == list:
                list_dist_obj = ListsDistance(freq_per_attribute=self.freq_per_attribute[attr],
                                              list1=val, list2=self.instance_b[attr],
                                              lists_dist_method=self.lists_dist_method)

                list_dist_result = list_dist_obj.calc_dist()
                self.categorical_sum += list_dist_result

                print(val_type)
                print(f'attr {attr}')
                print(f'list dist result {list_dist_result}\n')
                print("####################################################################################")

            elif val_type == dict:
                nested_dist_obj = NestedDistance(freq_per_attribute=self.freq_per_attribute[attr], attribute=attr,
                                                 nested_obj1=val, nested_obj2=self.instance_b[attr])
                nested_dist_obj.calc_dist()

        print(f'categorical sum result {self.categorical_sum}')
        print(f'numerical sum result {self.numerical_sum}')

    def q14(self):
        return math.sqrt(self.categorical_sum + self.numerical_sum)

    def calc_distance(self):

        print(f'attr types {self.attr_types}')
        print(f'nested attr types {self.nested_attr_types}')
        # print(f'freq per attr {self.freq_per_attribute}')
        # print(f'domain per attr {self.domain_per_attribute}')
        #
        # self.instance_a = {attr: self.instance_a[inx] for inx, attr in enumerate(self.attr_types.keys())}
        # self.instance_b = {attr: self.instance_b[inx] for inx, attr in enumerate(self.attr_types.keys())}
        print(f'instance a - {self.instance_a}')
        print(f'instance b - {self.instance_b}')

        self.q11()
        # print(f'total distance result {self.q14()}')
        return self.q14()


if __name__ == '__main__':
    interest = {'web applications': 2, 'web development': 4,
                'programming': 3, 'entrepreneurship': 3}


