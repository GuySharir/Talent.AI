import os
from program.ReadData import read_local_json_employees, read_attr_types_data, read_nested_attr_types_data
from pydoc import locate
import matplotlib.pyplot as plt
import statistics
import numpy as np


class LengthAttr:
    def __init__(self, df, attr_types, nested_attr_types):
        self.df = df
        self.attr_types = attr_types
        self.nested_attr_types = nested_attr_types

        self.lis_lengths_per_attr = {}
        self.nested_lengths_per_attr = {}

        self.lis_lengths_per_attr_min_max = {}
        self.nested_lengths_per_attr_min_max = {}

    def nested_length(self, instance: list, nested_attr: str):
        nested_length = len(instance)
        if nested_attr in self.nested_lengths_per_attr:
            self.nested_lengths_per_attr[nested_attr].append(nested_length)
        else:
            self.nested_lengths_per_attr[nested_attr] = [nested_length]

        for nested_obj in instance:
            for attr, val in nested_obj.items():
                val_type = locate(self.nested_attr_types[nested_attr][attr].split("'")[1])
                if val_type == list:
                    self.lists_length(val=val, attr=nested_attr + ':' + attr)

    def lists_length(self, val: list, attr: str):
        list_length = len(val)
        if attr in self.lis_lengths_per_attr:
            self.lis_lengths_per_attr[attr].append(list_length)
        else:
            self.lis_lengths_per_attr[attr] = [list_length]

    def length_check_per_attr(self):

        for i in range(0, len(self.df)):
            instance = {attr: self.df.iloc[i][inx] for inx, attr in enumerate(self.attr_types.keys())}

            for attr, val in instance.items():
                val_type = locate(self.attr_types[attr].split("'")[1])
                if val_type == list:
                    self.lists_length(val=val, attr=attr)
                elif val_type == dict:
                    self.nested_length(instance=val, nested_attr=attr)

        # print(f'lists length {self.lis_lengths_per_attr}')
        # print(f'nested length {self.nested_lengths_per_attr}')

        self.lis_lengths_per_attr_min_max = {key: {'min': min(val), 'max': max(val), 'median': statistics.median(val)} for key, val in self.lis_lengths_per_attr.items()}
        self.nested_lengths_per_attr_min_max = {key: {'min': min(val), 'max': max(val), 'median': statistics.median(val)} for key, val in self.nested_lengths_per_attr.items()}

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'dataTool\\runtimeObjectsInfo')).replace('/', '\\')
        length_path = os.path.abspath(os.path.join(path, 'number_of_elements.txt'))

        with open(length_path, 'w') as f:
            f.write(f'lists: {self.lis_lengths_per_attr_min_max}\nnested: {self.nested_lengths_per_attr_min_max}')

        for key, val in self.lis_lengths_per_attr.items():
            plt.title(key)
            bins = np.unique(val)
            plt.hist(val, bins=bins)
            plt.show()


if __name__ == '__main__':
    df_ = read_local_json_employees()
    attr_types_ = read_attr_types_data()
    nested_attr_types_ = read_nested_attr_types_data()

    obj = LengthAttr(df=df_, attr_types=attr_types_, nested_attr_types=nested_attr_types_)
    obj.length_check_per_attr()
