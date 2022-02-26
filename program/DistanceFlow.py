import os
import pandas as pd
import numpy as np
from algorithems.domain_size_frequencies import DomainAndFrequency


class DistanceFlow:
    """
        This class (DistanceFlow) is responsible for the distance calculation flow

        starting with data cleaning (in the re-processing phase)
        frequencies and domain size calculation (every periodical phase) - when DB changes
        calculate distance matrix for each data set in the data base

        - self.df, represents all employees data from json files
    """
    def __init__(self):
        self.df = None
        self.domain_per_attribute = {}
        self.freq_per_attribute = {}

    def calc_domain_and_frequency(self):
        attributes = {}
        types = [str, int, float, dict, list]
        data_path = os.path.abspath(os.path.
                                    join(os.path.dirname(__file__), '..', 'dataTool\\clean_data')).replace('/', '\\')
        print(f'data path', data_path)
        adobe = os.path.join(data_path, 'AdobeEmployees.json')
        with open(adobe) as f:
            self.df = pd.read_json(f)
            for attr in self.df.keys():
                data_type = type(self.df.iloc[0][attr])
                if data_type == list:
                    if type(self.df.iloc[0][attr][0]) == dict:
                        data_type = dict
                elif data_type == np.float64:
                    data_type = float
                if data_type not in types:
                    print(f'unpredicted value type')

                attributes[attr] = data_type
            print(f'attributes dict {attributes}')

        for attr, val_type in attributes.items():
            print(f'attribute {attr}')
            DomainAndFrequency(attr=attr, val_type=val_type, data_frame=self.df).calc_domain_and_frequency()


if __name__ == '__main__':
    DistanceFlow().calc_domain_and_frequency()
