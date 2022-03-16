import math
import numpy as np
from pydoc import locate

from distance.DistanceData import NestedDistanceData, DistanceFunctionalityData
from distance.DistEnum import ListDistMethod, NestedDistMethod
from distance.DistanceFunctions import DistanceNumStr


class NestedDistance:
    def __init__(self, nested_distance_data: NestedDistanceData):
        self.nested_distance_data = nested_distance_data

    def recursive_obj_dist(self) -> float:
        # print(f'attribute-  {self.nested_distance_data.attribute}')
        # print(f'obj1- {self.nested_distance_data.obj1}')
        # print(f'obj2- {self.nested_distance_data.obj2}')

        obj2_num_of_items = len(self.nested_distance_data.obj2)
        obj1_num_of_items = len(self.nested_distance_data.obj1)
        print(f'number of items in object2- {obj2_num_of_items}')
        print(f'number of items in object1- {obj1_num_of_items}')

        matrix_scores = np.empty((0, obj2_num_of_items), float)
        for inx1 in range(obj1_num_of_items):
            row = []  # number of rows represent number of items in nested obj1
            val1 = self.nested_distance_data.obj1[inx1]

            for inx2 in range(obj2_num_of_items):
                val2 = self.nested_distance_data.obj2[inx2]
                dist_data = DistanceFunctionalityData(instance_a=val1, instance_b=val2, attr_types=self.nested_distance_data.nested_attr_types[self.nested_distance_data.attribute],
                                                      nested_attr_types={},
                                                      freq_per_attribute=self.nested_distance_data.value_frequency,
                                                      domain_per_attribute=self.nested_distance_data.domain_size,
                                                      lists_dist_method=self.nested_distance_data.lists_dist_method,
                                                      nested_dist_method=self.nested_distance_data.nested_dist_method)
                distance = DistanceFunctionality().calc_distance(data=dist_data)
                row.append(distance)
            print(row)
            matrix_scores = np.append(matrix_scores, np.array([row]), axis=0)

        print(f'matrix_scores- {matrix_scores}')
        print(f'matrix_scores sum- {matrix_scores.sum()}')
        return matrix_scores.sum()

    def education_dist(self) -> float:
        if self.nested_distance_data.nested_dist_method == NestedDistMethod.all_items:
            return self.recursive_obj_dist()

    def experience_dist(self) -> float:
        if self.nested_distance_data.nested_dist_method == NestedDistMethod.all_items:
            return self.recursive_obj_dist()

    def calc_dist(self) -> float:
        print("################################# Nested Attribute ########################################")
        if self.nested_distance_data.attribute == 'education':
            return self.education_dist()
        elif self.nested_distance_data.attribute == 'experience':
            return self.experience_dist()


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

    def __init__(self):

        self.categorical_sum = 0
        self.numerical_sum = 0
        self.nested_sum = 0

    def q11(self, data: DistanceFunctionalityData):

        for attr, val in data.instance_a.items():
            val_type = locate(data.attr_types[attr].split("'")[1])
            dist_obj = DistanceNumStr()
            if val_type == str:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val, val2=data.instance_b[attr],
                                                    value_frequency=data.freq_per_attribute[attr],
                                                    domain_size=data.domain_per_attribute[attr],
                                                    attribute=attr, instance_a=data.instance_a,
                                                    instance_b=data.instance_b)
                self.categorical_sum += result

            elif val_type == float or val_type == int:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val,
                                                    val2=data.instance_b[attr],
                                                    value_frequency=data.freq_per_attribute[attr],
                                                    domain_size=data.domain_per_attribute[attr], attribute=attr)
                self.numerical_sum += result

            elif val_type == list:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val,
                                                    val2=data.instance_b[attr],
                                                    value_frequency=data.freq_per_attribute[attr],
                                                    domain_size=data.domain_per_attribute[attr], attribute=attr,
                                                    instance_a=None, instance_b=None,
                                                    lists_dist_method=data.lists_dist_method)
                self.categorical_sum += result

            elif val_type == dict:
                nested_data = NestedDistanceData(val_type=val_type, obj1=val, obj2=data.instance_b[attr],
                                                 value_frequency=data.freq_per_attribute[attr],
                                                 domain_size=data.domain_per_attribute[attr],
                                                 attribute=attr, instance_a=data.instance_a, instance_b=data.instance_b,
                                                 lists_dist_method=data.lists_dist_method,
                                                 nested_dist_method=data.nested_dist_method,
                                                 nested_attr_types=data.nested_attr_types)

                nested_dist_obj = NestedDistance(nested_distance_data=nested_data)
                result = nested_dist_obj.calc_dist()
                self.nested_sum += result

        print(f'nested sum result {self.nested_sum}')
        print(f'categorical sum result {self.categorical_sum}')
        print(f'numerical sum result {self.numerical_sum}')

    def q14(self) -> float:
        print(f'total distance sum {math.sqrt(self.categorical_sum + self.numerical_sum)}')
        return math.sqrt(self.categorical_sum + self.numerical_sum)

    def calc_distance(self, data: DistanceFunctionalityData) -> float:

        print(f'attr types {data.attr_types}')
        print(f'nested attr types {data.nested_attr_types}')
        print(f'instance a - {data.instance_a}')
        print(f'instance b - {data.instance_b}')

        self.q11(data)

        return self.q14()


if __name__ == '__main__':
    pass

