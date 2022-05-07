import os
from pydoc import locate
import pandas as pd

from ReadData import read_nested_attr_types_data


def logger(*args):
    # print(*args)
    pass


class DomainAndFrequency:
    """
        This class (Attribute) is responsible to calculate the frequency fo each possible value for
        the given categorical attribute and the attribute domain size
        - self.attr, the attribute
        - self.domain_size, domain size of a given attribute (the number of possible values for the given attribute)
        - self.value_frequency, the frequency of a possible value in the given attribute
        - self.attr_values, list of the possible values in the given attribute
        - self.attr_values_dict, dict of lists of the possible values in a given attribute in case of nested attribute
        - self.val_type, indicates whether the attribute value is str, list or nested

        the return value is the frequency for each value and the attribute domain size
    """

    def __init__(self, attr, val_type, data_frame):
        self.df = data_frame
        self.attr = attr
        self.val_type = val_type
        self.domain_size = None
        self.attr_values = []
        self.attr_values_dict = {}
        self.value_frequency = {}

    @staticmethod
    def iteration(values_list: list, freq_dict: dict, val) -> tuple:
        if type(val) == list:
            for item in val:
                if item not in values_list:
                    values_list.append(item)

                if item not in freq_dict.keys():
                    freq_dict[item] = 1
                else:
                    freq_dict[item] += 1
        else:
            if type(val) == str and not val:
                val = 'null'
            if val not in values_list:
                values_list.append(val)

            if val not in freq_dict.keys():
                freq_dict[val] = 1
            else:
                freq_dict[val] += 1

        return values_list, freq_dict

    def str_values(self):
        for _, row in self.df.iterrows():
            self.attr_values, self.value_frequency = \
                self.iteration(self.attr_values, self.value_frequency, row[self.attr])
        self.domain_size = len(self.attr_values)

    def list_values(self):
        for _, row in self.df.iterrows():
            for value in row[self.attr]:
                self.attr_values, self.value_frequency = \
                    self.iteration(self.attr_values, self.value_frequency, value)
            self.domain_size = len(self.attr_values)

    def nested_values(self):
        nested_attr_type = read_nested_attr_types_data()
        nested_attr_type = nested_attr_type[self.attr]
        logger(nested_attr_type)

        # attr_list = {'company_name': ['adobe', 'linkedin', ....], size: [], ...}
        # attr_freq = {'company_name': {'adobe': 6, 'linkedin': 2}}
        attr_list = {}
        attr_freq = {}

        for _, row in self.df.iterrows():
            for value in row[self.attr]:
                for key, val in value.items():
                    nested_type = locate((nested_attr_type[key]).split("'")[1])
                    if nested_type == bool or nested_type == str or nested_type == list:
                        if key not in attr_freq.keys():
                            result = self.iteration([], {}, val)
                        else:
                            result = self.iteration(attr_list[key], attr_freq[key], val)

                        attr_list[key] = result[0]
                        attr_freq[key] = result[1]

        self.domain_size = {}
        self.value_frequency = attr_freq
        self.attr_values_dict = attr_list
        self.domain_size = {attr: len(self.attr_values_dict[attr]) for attr in self.attr_values_dict.keys()}

    def calc_domain_and_frequency(self):
        if self.val_type == str:
            self.str_values()
        elif self.val_type == list:
            self.list_values()
        elif self.val_type == dict:
            self.nested_values()

        # logger(f'val frequency {self.value_frequency}')
        # logger(f'attribute values {self.attr_values}')
        # logger(f'attribute values dict {self.attr_values_dict}')
        # logger(f'domain size {self.domain_size}')

        return self.value_frequency, self.domain_size


if __name__ == '__main__':
    def read_employee_data():
        data_path = os.path.abspath(os.path.
                                    join(os.path.dirname(__file__), '..', 'dataTool\\clean_data')).replace('/', '\\')
        logger(f'data path', data_path)
        adobe = os.path.join(data_path, 'AdobeEmployees.json')
        # adobe = os.path.join(data_path, 'Demo.json')
        df = pd.read_json(adobe)
        return df


    data = read_employee_data()
    freq, size = DomainAndFrequency('experience', dict, data).calc_domain_and_frequency()
    logger(freq, size)
    # DomainAndFrequency('skills', list).calc_domain_and_frequency()
    # DomainAndFrequency('gender', str).calc_domain_and_frequency()
