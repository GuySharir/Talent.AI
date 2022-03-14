from distance.DistanceData import ListDistanceData, NumDistanceData, StrDistanceData, NestedDistanceData
from distance.DistEnum import NestedDistMethod
from distance.DistanceFunctions import DistanceNumStr
import numpy as np
from pydoc import locate


class NestedDistance:
    def __init__(self, nested_distance_data: NestedDistanceData):
        self.nested_distance_data = nested_distance_data

    def call_attr_distance_calc(self, val1: dict, val2: dict) -> float:
        distance_sum = 0
        dist_obj = DistanceNumStr()
        att_type = self.nested_distance_data.nested_attr_types[self.nested_distance_data.attribute]

        for attr, val in val1.items():
            val_type = locate(att_type[attr].split("'")[1])
            print(val_type)
            if val_type == str:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val, val2=val2[attr],
                                                    value_frequency=self.nested_distance_data.value_frequency[attr],
                                                    domain_size=self.nested_distance_data.domain_size[attr],
                                                    attribute=attr, instance_a=val1,
                                                    instance_b=val2)
                print(f'result- {result}')
                distance_sum += result

            elif val_type == float or val_type == int:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val, val2=val2[attr],
                                                    value_frequency=self.nested_distance_data.value_frequency[attr],
                                                    domain_size=self.nested_distance_data.domain_size[attr],
                                                    attribute=attr)
                print(f'result- {result}')
                distance_sum += result

            elif val_type == list:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val, val2=val2[attr],
                                                    value_frequency=self.nested_distance_data.value_frequency[attr],
                                                    domain_size=self.nested_distance_data.domain_size[attr],
                                                    attribute=attr, instance_a=None, instance_b=None,
                                                    lists_dist_method=self.nested_distance_data.lists_dist_method)
                print(f'result- {result}')
                distance_sum += result
        return distance_sum

    def calc_nested_obj_matrix(self) -> float:

        print(f'attribute-  {self.nested_distance_data.attribute}')
        print(f'obj1- {self.nested_distance_data.obj1}')
        print(f'obj2- {self.nested_distance_data.obj2}')

        obj2_num_of_items = len(self.nested_distance_data.obj2)
        obj1_num_of_items = len(self.nested_distance_data.obj1)
        print(f'number of items in object2- {obj2_num_of_items}')
        print(f'number of items in object1- {obj1_num_of_items}')

        matrix_scores = np.empty((0, obj2_num_of_items), float)
        for inx1 in range(obj1_num_of_items):
            row = []  # number of rows represent number of items in nested obj1
            val1 = self.nested_distance_data.obj1[inx1]
            print(val1)
            for inx2 in range(obj2_num_of_items):
                val2 = self.nested_distance_data.obj2[inx2]
                row.append(self.call_attr_distance_calc(val1=val1, val2=val2))
            print(row)
            matrix_scores = np.append(matrix_scores, np.array([row]), axis=0)

        print(f'matrix_scores- {matrix_scores}')
        print(f'matrix_scores sum- {matrix_scores.sum()}')
        return matrix_scores.sum()

    def calc_dist(self) -> float:
        print("################################# Nested Attribute ########################################")
        if self.nested_distance_data.attribute == 'education':
            return self.education_dist()
        elif self.nested_distance_data.attribute == 'experience':
            return self.experience_dist()

    def education_dist(self) -> float:
        if self.nested_distance_data.nested_dist_method == NestedDistMethod.all_items:
            return self.calc_nested_obj_matrix()

    def experience_dist(self) -> float:
        if self.nested_distance_data.nested_dist_method == NestedDistMethod.all_items:
            return self.calc_nested_obj_matrix()


