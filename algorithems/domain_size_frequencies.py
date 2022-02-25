import os
import pandas as pd


class Attribute:
    """
        This class (Attribute) is responsible to calculate the frequency fo each possible value for
        the given categorical attribute and the attribute domain size
        - self.attr, the attribute
        - self.domain_size, domain size of a given attribute (the number of possible values for the given attribute)
        - self.value_frequency, the frequency of a possible value in the given attribute
        - self.attr_values, list of the possible values in the given attribute
        - self.val_type, indicates whether the attribute value is str, list or nested

        the return value is the frequency for each value and the attribute domain size
    """
    def __init__(self, attr, val_type):
        self.attr = attr
        self.val_type = val_type
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

    def str_values(self, df):
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

    def list_values(self, df):
        for _, row in df.iterrows():
            print(f'adobe df {row[self.attr]}')
            for value in row[self.attr]:
                if value not in self.attr_values:
                    self.attr_values.append(value)

                if value not in self.value_frequency.keys():
                    self.value_frequency[value] = 1
                else:
                    self.value_frequency[value] += 1
        print(f'val frequency {self.value_frequency}')
        print(f'attribute values {self.attr_values}')

        self.domain_size = len(self.attr_values)
        print(f'domain size {self.domain_size}')

    def nested_values(self, df):
        pass

    def calc_domain_and_frequency(self):
        df = self.read_employee_data()
        if self.val_type == str:
            self.str_values(df)
        elif self.val_type == list:
            self.list_values(df)
        elif self.val_type == dict:
            pass
        return self.value_frequency, self.domain_size


if __name__ == '__main__':
    Attribute('interests', list).calc_domain_and_frequency()
