from distance.DistEnum import NestedDistMethod
import numpy as np


class NestedDistance:
    def __init__(self, freq_per_attribute: dict, attribute: list, nested_obj1: dict, nested_obj2,
                 nested_dist_method: NestedDistMethod):
        self.freq_per_attribute = freq_per_attribute
        self.attribute = attribute
        self.nested_obj1 = nested_obj1
        self.nested_obj2 = nested_obj2
        self.nested_dist_method = nested_dist_method

    def calc_nested_obj_matrix(self):
        print(f"degrees values {self.freq_per_attribute['degrees']}")
        print(f"majors values {self.freq_per_attribute['majors']}")
        print(f"unique values from major {set(self.freq_per_attribute['majors'])}")

        print(f'attr {self.attribute}')
        print(f'obj1 {self.nested_obj1}')
        print(f'obj2 {self.nested_obj2}')

        obj2_num_of_items = len(self.nested_obj2)
        obj1_num_of_items = len(self.nested_obj1)
        print(f'number of items in object2- {obj2_num_of_items}')
        print(f'number of items in object1- {obj1_num_of_items}')

        matrix_scores = np.empty((0, obj2_num_of_items), float)
        for inx1 in range(obj1_num_of_items):
            row = []  # number of rows represent number of items in nested obj1
            for inx2 in range(obj2_num_of_items):
                row.append(1)
            print(row)
            matrix_scores = np.append(matrix_scores, np.array([row]), axis=0)

        print(f'matrix_scores- {matrix_scores}')
        print(f'matrix_scores sum- {matrix_scores.sum()}')

    def calc_dist(self):
        if self.attribute == 'education':
            self.education_dist()
        elif self.attribute == 'experience':
            self.experience_dist()

    def education_dist(self):
        if self.nested_dist_method == NestedDistMethod.all_items:
            self.calc_nested_obj_matrix()

    def experience_dist(self):
        pass
        # if self.nested_dist_method == NestedDistMethod.all_items:
        #     self.calc_nested_obj_matrix()


