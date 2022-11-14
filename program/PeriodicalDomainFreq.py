import json
import os
from pydoc import locate
from program.ReadData import read_attr_types_data, read_local_json_employees
from program.DomainSizeFrequencies import DomainAndFrequency
import pandas as pd


def logger(*args):
    # print(*args)
    pass


class DomainFreqCalc:
    def __init__(self, df: pd.DataFrame):
        self.attr_types = read_attr_types_data()

        self.df = df
        self.domain_per_attribute = {}
        self.freq_per_attribute = {}

    @staticmethod
    def set_path(name):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{name}')) \
            .replace('/', '/')
        return path

    def calc_domain_freq_per_value(self):
        self.attr_types = read_attr_types_data()

        for attr, val_type in self.attr_types.items():
            val_type = locate(val_type.split("'")[1])
            logger(f'attribute {attr}')
            value_frequency, domain_size = \
                DomainAndFrequency(attr=attr, val_type=val_type,
                                   data_frame=self.df).calc_domain_and_frequency()

            self.domain_per_attribute.update({attr: domain_size})
            self.freq_per_attribute.update({attr: value_frequency})

        domain_size_path = self.set_path('dataTool/domain_size')
        domain_path = os.path.abspath(os.path.join(
            domain_size_path, 'attributes_domain_size.json'))
        with open(domain_path, 'w') as fp:
            json.dump(self.domain_per_attribute, fp)

        freq_path = self.set_path('dataTool/frequencies')
        frequencies_path = os.path.abspath(
            os.path.join(freq_path, 'attributes_frequency.json'))
        with open(frequencies_path, 'w') as fp:
            json.dump(self.freq_per_attribute, fp)


if __name__ == '__main__':
    df_ = read_local_json_employees()
    DomainFreqCalc(df=df_).calc_domain_freq_per_value()
