import os
import pandas as pd


class Attribute:
    """
        This class (Attribute) is responsible to calculate the frequency fo each possible value for
        the given attribute and the attribute domain size
        - self.attr, the attribute
        - self.domain_size, domain size of a given attribute (the number of possible values for the given attribute)
        - self.value_frequency, the frequency of a possible value in the given attribute
        - self.attr_values. list of the possible values in the given attribute
    """
    def __init__(self, attr):
        self.attr = attr
        self.domain_size = None
        self.attr_values = []
        self.value_frequency = {}

    @staticmethod
    def read_employee_data():
        data_path = os.path.abspath(os.path.
                                    join(os.path.dirname(__file__), '..', 'dataTool\\clean_data')).replace('/', '\\')
        print(f'data path', data_path)
        adobe = os.path.join(data_path, 'AdobeEmployees.json')
        df = pd.read_json(adobe)
        return df

    def calc_domain_and_frequency(self):
        df = self.read_employee_data()
        for _, row in df.iterrows():
            print(f'adobe df {row[self.attr]}')
            if row[self.attr] not in self.attr_values:
                self.attr_values.append(row[self.attr])

            if row[self.attr] not in self.value_frequency.keys():
                self.value_frequency[row[self.attr]] = 1
            else:
                self.value_frequency[row[self.attr]] += 1
        print(f'val frequency {self.value_frequency}')
        print(f'attribute values {self.attr_values}')

        self.domain_size = len(self.attr_values)
        print(f'domain size {self.domain_size}')


if __name__ == '__main__':
    Attribute('birth_date').calc_domain_and_frequency()
