import os
import json
import pandas as pd
import numpy as np
from algorithems.domain_size_frequencies import DomainAndFrequency
from algorithems.DistanceCalc import Distance


class DistanceFlow:
    """
        This class (DistanceFlow) is responsible for the distance calculation flow

        starting with data cleaning (in the re-processing phase)
        frequencies and domain size calculation (every periodical phase) - when DB changes
        calculate distance matrix for each data set in the data base

        - self.df, represents all employees data from json files
        - self.domain_per_attribute, for each attribute in the data represent its domain size
        (the number of possible values)
        - self.freq_per_attribute, for each attributes' value in the data represent its frequency
    """
    def __init__(self, calc_domain_freq=False):
        self.df = None
        self.calc_domain_freq = calc_domain_freq
        self.domain_per_attribute = {}
        self.freq_per_attribute = {}
        self.attr_types = {}

    def open_json_and_attr_types(self):
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

                self.attr_types[attr] = data_type
            print(f'attributes dict {self.attr_types}')

    def calc_domain_and_frequency(self):
        for attr, val_type in self.attr_types.items():
            print(f'attribute {attr}')
            value_frequency, domain_size =\
                DomainAndFrequency(attr=attr, val_type=val_type, data_frame=self.df).calc_domain_and_frequency()

            self.domain_per_attribute.update({attr: domain_size})
            self.freq_per_attribute.update({attr: value_frequency})
        print(f'domain per attribute {self.domain_per_attribute}')
        print(f'freq per attribute {self.freq_per_attribute}')

        domain_size_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataTool\\domain_size'))\
            .replace('/', '\\')
        domain_path = os.path.abspath(os.path.join(domain_size_path, 'attributes_domain_size.json'))
        with open(domain_path, 'w') as fp:
            json.dump(self.domain_per_attribute, fp)

        freq_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataTool\\frequencies'))\
            .replace('/', '\\')
        frequencies_path = os.path.abspath(os.path.join(freq_path, 'attributes_frequency.json'))
        with open(frequencies_path, 'w') as fp:
            json.dump(self.freq_per_attribute, fp)

    def run_distance_flow(self):
        self.open_json_and_attr_types()
        if self.calc_domain_freq:
            print('here')
            self.calc_domain_and_frequency()
        # print(self.df.iloc[0][0])
        # print(type(self.df.iloc[0]))
        Distance(self.df.iloc[0], self.df.iloc[1], self.attr_types).calc_distance()


if __name__ == '__main__':
    DistanceFlow(False).run_distance_flow()
