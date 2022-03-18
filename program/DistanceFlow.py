import os
import json
import pandas as pd
import numpy as np
from pydoc import locate
from datetime import datetime
from distance.DistEnum import ListDistMethod
from distance.DistEnum import NestedDistMethod
from distance.DistanceData import DistanceFunctionalityData
from distance.DomainSizeFrequencies import DomainAndFrequency
from distance.DistanceFunctionality import DistanceFunctionality


def my_print(*args):
    print(*args)


class DistanceFlow:
    """
        This class (DistanceFlow) is responsible for the distance calculation flow

        starting with data cleaning (in the re-processing phase)
        frequencies and domain size calculation (every periodical phase) - when DB changes
        manage attributes type and save it to json file
        calculate distance matrix for each data set in the DB

        - self.df, represents all employees data from json files

        - self.domain_per_attribute, for each attribute in the data represent its domain size
            (the number of possible values)

        - self.freq_per_attribute, for each attributes' value in the data represent its frequency

        - self.attr_types, represent attributes types
            {name: <str>, experience: dict, ..}

        - self.nested_attr_types, represent nested attributes types
            {experience:{company_name: <str>, company_size: <float>, ...}}
    """

    def __init__(self, calc_domain_freq=False, calc_attr_type=False,
                 lists_dist_method: ListDistMethod = ListDistMethod.intersection,
                 nested_dist_method: NestedDistMethod = NestedDistMethod.all_items):

        self.res = []
        self.df = None
        self.calc_domain_freq = calc_domain_freq
        self.calc_attr_type = calc_attr_type
        self.domain_per_attribute = {}
        self.freq_per_attribute = {}
        self.attr_types = {}
        self.nested_attr_types = {}

        self.lists_dist_method = lists_dist_method
        self.nested_dist_method = nested_dist_method

    @staticmethod
    def set_path(name):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{name}')) \
            .replace('/', '/')
        return path

    def read_json_employees(self):
        data_path = self.set_path('dataTool/clean_data')
        # data_path = os.path.abspath(os.path.
        #                             join(os.path.dirname(__file__), '..', 'dataTool\\clean_data')).replace('/', '\\')
        my_print(f'data path', data_path)

        all_files = [os.path.join(data_path, 'AppleEmployees.json'),
                     # os.path.join(data_path, 'AmazonEmployees.json'),
                     # os.path.join(data_path, 'AdobeEmployees.json'),
                     os.path.join(data_path, 'FacebookEmployees.json'),
                     # os.path.join(data_path, 'TwitterEmployees.json'),
                     # os.path.join(data_path, 'TeslaEmployees.json'),
                     # os.path.join(data_path, 'GoogleEmployees.json'),
                     # os.path.join(data_path, 'IbmEmployees.json'),
                     # os.path.join(data_path, 'MicrosoftEmployees.json'),
                     # os.path.join(data_path, 'NvidiaEmployees.json'),
                     # os.path.join(data_path, 'OracleEmployees.json'),
                     # os.path.join(data_path, 'SalesforceEmployees.json'),
                     # os.path.join(data_path, 'UberEmployees.json')
                     ]
        # all_files = [os.path.join(data_path, 'TwitterEmployees.json'),
        #              os.path.join(data_path, 'TeslaEmployees.json')]
        li = []
        for filename in all_files:
            with open(filename) as f:
                df = pd.read_json(f)
                li.append(df)

        self.df = pd.concat(li, axis=0, ignore_index=True)
        self.df = self.df.sample(n=30)
        my_print(self.df)

    def read_attr_domain(self):
        domain_size_path = self.set_path('dataTool/domain_size')
        domain_path = os.path.abspath(os.path.join(
            domain_size_path, 'attributes_domain_size.json'))
        with open(domain_path) as fp:
            self.domain_per_attribute = json.load(fp)

    def read_attr_freq(self):
        freq_path = self.set_path('dataTool/frequencies')
        frequencies_path = os.path.abspath(
            os.path.join(freq_path, 'attributes_frequency.json'))
        with open(frequencies_path) as fp:
            self.freq_per_attribute = json.load(fp)

    def read_attr_types(self):
        path = self.set_path('dataTool/attributes_types')
        attribute_type_path = os.path.abspath(
            os.path.join(path, 'attributes_types.json'))
        attribute_nested_type_path = os.path.abspath(os.path.join(path,
                                                                  'nested_attributes_types.json'))
        with open(attribute_type_path) as f:
            self.attr_types = json.load(f)

        with open(attribute_nested_type_path) as f:
            self.nested_attr_types = json.load(f)

    def calc_domain_and_frequency(self):
        if not self.attr_types:
            self.read_attr_types()

        for attr, val_type in self.attr_types.items():
            val_type = locate(val_type.split("'")[1])
            my_print(f'attribute {attr}')
            value_frequency, domain_size = \
                DomainAndFrequency(attr=attr, val_type=val_type,
                                   data_frame=self.df).calc_domain_and_frequency()

            self.domain_per_attribute.update({attr: domain_size})
            self.freq_per_attribute.update({attr: value_frequency})
        my_print(f'domain per attribute {self.domain_per_attribute}')
        my_print(f'freq per attribute {self.freq_per_attribute}')

        domain_size_path = self.set_path('dataTool/domain_size')
        # domain_size_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataTool/domain_size'))\
        #     .replace('/', '/')
        domain_path = os.path.abspath(os.path.join(
            domain_size_path, 'attributes_domain_size.json'))
        with open(domain_path, 'w') as fp:
            json.dump(self.domain_per_attribute, fp)

        freq_path = self.set_path('dataTool/frequencies')
        # freq_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataTool/frequencies'))\
        #     .replace('/', '/')
        frequencies_path = os.path.abspath(
            os.path.join(freq_path, 'attributes_frequency.json'))
        with open(frequencies_path, 'w') as fp:
            json.dump(self.freq_per_attribute, fp)

    def calc_nested_attribute_type(self):
        attributes = [attr for attr in self.df.keys()]
        nested_attr_type = {}

        for inx, val in enumerate(self.df.iloc[0]):
            attr_type = {}
            if val and type(val) == list and type(val[0]) == dict:
                for key, item in val[0].items():
                    attr_type[key] = str(type(item))
                nested_attr_type.update({attributes[inx]: attr_type})

        self.nested_attr_types.update(nested_attr_type)

    def calc_attributes_type(self):
        types = [str, int, float, dict, list]

        for attr in self.df.keys():
            data_type = type(self.df.iloc[0][attr])
            if data_type == list:
                if type(self.df.iloc[0][attr][0]) == dict:
                    data_type = dict
            elif data_type == np.float64:
                data_type = float
            if data_type not in types:
                my_print(f'Error! unpredicted value type')

            self.attr_types[attr] = str(data_type)

        self.calc_nested_attribute_type()
        my_print(f'all attributes type- {self.attr_types}')

        path = self.set_path('dataTool/attributes_types')
        attribute_type_path = os.path.abspath(
            os.path.join(path, 'attributes_types.json'))
        attribute_nested_type_path = os.path.abspath(os.path.join(path,
                                                                  'nested_attributes_types.json'))
        with open(attribute_type_path, 'w') as fp:
            json.dump(self.attr_types, fp)

        with open(attribute_nested_type_path, 'w') as fp:
            json.dump(self.nested_attr_types, fp)

    def df_row_to_instance(self, index) -> dict:
        return {attr: self.df.iloc[index][inx] for inx, attr in enumerate(self.attr_types.keys())}

    def list_to_instance(self, obj: list) -> dict:
        return {attr: obj[inx] for inx, attr in enumerate(self.attr_types.keys())}

    def dis_for_clustering(self, instance_a: list, instance_b: list) -> list:
        # if instance_a and instance_b:
        if self.calc_domain_freq:
            self.calc_domain_and_frequency()
        else:
            self.read_attr_types()
            self.read_attr_domain()
            self.read_attr_freq()

        instance_a = self.list_to_instance(obj=instance_a)
        instance_b = self.list_to_instance(obj=instance_b)
        print(f"{instance_a['full_name']} VS {instance_b['full_name']}")
        distance_obj = DistanceFunctionalityData(instance_a=instance_a, instance_b=instance_b,
                                                 attr_types=self.attr_types,
                                                 nested_attr_types=self.nested_attr_types,
                                                 freq_per_attribute=self.freq_per_attribute,
                                                 domain_per_attribute=self.domain_per_attribute,
                                                 lists_dist_method=self.lists_dist_method,
                                                 nested_dist_method=self.nested_dist_method)
        self.res.append(DistanceFunctionality(
        ).calc_distance(data=distance_obj))
        return self.res

    def run_distance_flow(self, loop=False) -> list:
        self.read_json_employees()
        if self.calc_attr_type:
            self.calc_attributes_type()
        if self.calc_domain_freq:
            self.calc_domain_and_frequency()
        else:
            self.read_attr_types()
            self.read_attr_domain()
            self.read_attr_freq()

        # self.res = np.zeros((len(self.df), len(self.df)))

        if loop:
            for i in range(0, len(self.df)):
                for j in range(i, len(self.df)):
                    instance_a = self.df_row_to_instance(i)
                    instance_b = self.df_row_to_instance(j)
                    print(f"in loop: {instance_a['full_name']} VS {instance_b['full_name']}")
                    distance_data_obj = DistanceFunctionalityData(instance_a=instance_a, instance_b=instance_b,
                                                                  attr_types=self.attr_types,
                                                                  nested_attr_types=self.nested_attr_types,
                                                                  freq_per_attribute=self.freq_per_attribute,
                                                                  domain_per_attribute=self.domain_per_attribute,
                                                                  lists_dist_method=self.lists_dist_method,
                                                                  nested_dist_method=self.nested_dist_method)

                    self.res[i][j] = self.res[j][i] = DistanceFunctionality() \
                        .calc_distance(distance_data_obj)
        else:
            instance_a = self.df_row_to_instance(1)
            instance_b = self.df_row_to_instance(5)
            distance_data_obj = DistanceFunctionalityData(instance_a=instance_a, instance_b=instance_b,
                                                          attr_types=self.attr_types,
                                                          nested_attr_types=self.nested_attr_types,
                                                          freq_per_attribute=self.freq_per_attribute,
                                                          domain_per_attribute=self.domain_per_attribute,
                                                          lists_dist_method=self.lists_dist_method,
                                                          nested_dist_method=self.nested_dist_method)
            self.res.append(DistanceFunctionality(
            ).calc_distance(data=distance_data_obj))

        return self.res


def main(dist_for_clustering=False, instance_a: list = None, instance_b: list = None):
    my_print(f'start time {datetime.now().strftime("%H:%M:%S")}')
    # choose to calculate domain and frequencies -> domain_and_freq = True means calculate
    # domain_and_freq = True
    domain_and_freq = True

    # choose to calculate attributes types -> attr_type = True means calculate
    # attr_type = True
    attr_type = False
    dist_obj = DistanceFlow(calc_domain_freq=domain_and_freq, calc_attr_type=attr_type,
                            lists_dist_method=ListDistMethod.intersection,
                            nested_dist_method=NestedDistMethod.all_items)

    if dist_for_clustering:
        res = dist_obj.dis_for_clustering(
            instance_a=instance_a, instance_b=instance_b)
    else:
        res = dist_obj.run_distance_flow()

    my_print(f'sum- {sum(res)}')
    my_print(f'unique val- {len(np.unique(res))}')
    my_print(f'distance res- {res}')
    my_print(f'min val res- {min(res)}')
    my_print(f'max val res- {max(res)}')

    my_print(f'end time {datetime.now().strftime("%H:%M:%S")}')


if __name__ == '__main__':
    # choose dist_for_clustering
    # dist_for_clustering = True
    # instance_a =
    # instance_b =

    main()

