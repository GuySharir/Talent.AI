import math
from pydoc import locate
from distance.ListsDistance import ListsDistance
from distance.NestedDistance import NestedDistance
from distance.DistEnum import ListDistMethod
from distance.DistEnum import NestedDistMethod
from distance.DistanceFunctions import DistanceNumStr


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
            dist_obj = DistanceNumStr()
            if val_type == str:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val, val2=self.instance_b[attr],
                                                    value_frequency=self.freq_per_attribute[attr],
                                                    domain_size=self.domain_per_attribute[attr],
                                                    attribute=attr, instance_a=self.instance_a,
                                                    instance_b=self.instance_b)
                self.categorical_sum += result

            elif val_type == float or val_type == int:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val,
                                                    val2=self.instance_b[attr],
                                                    value_frequency=self.freq_per_attribute[attr],
                                                    domain_size=self.domain_per_attribute[attr], attribute=attr)
                self.numerical_sum += result

            elif val_type == list:
                result = dist_obj.distance_per_type(val_type=val_type, val1=val,
                                                    val2=self.instance_b[attr],
                                                    value_frequency=self.freq_per_attribute[attr],
                                                    domain_size=self.domain_per_attribute[attr], attribute=attr,
                                                    instance_a=None, instance_b=None,
                                                    lists_dist_method=self.lists_dist_method)
                self.categorical_sum += result

            elif val_type == dict:
                nested_dist_obj = NestedDistance(freq_per_attribute=self.freq_per_attribute[attr], attribute=attr,
                                                 nested_obj1=val, nested_obj2=self.instance_b[attr],
                                                 nested_dist_method=self.nested_dist_method)
                nested_dist_obj.calc_dist()

        print(f'categorical sum result {self.categorical_sum}')
        print(f'numerical sum result {self.numerical_sum}')

    def q14(self):
        return math.sqrt(self.categorical_sum + self.numerical_sum)

    def calc_distance(self):

        print(f'attr types {self.attr_types}')
        print(f'nested attr types {self.nested_attr_types}')
        print(f'instance a - {self.instance_a}')
        print(f'instance b - {self.instance_b}')

        self.q11()

        return self.q14()


if __name__ == '__main__':
    pass

