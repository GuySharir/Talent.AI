from typing import List
from numpy import NaN, nan
import pandas as pd
import glob
import os
import sys
import math
import inspect
import time

THRESHOLD = 0.03

records = {}

numeric_data = ["birth_year", "job_company_founded"]

categorical_data = ['id', 'full_name', 'first_name', 'middle_initial', 'middle_name',
                    'last_initial', 'last_name', 'gender',
                    'linkedin_url', 'linkedin_username', 'linkedin_id', 'facebook_url',
                    'facebook_username', 'facebook_id', 'twitter_url', 'twitter_username',
                    'github_url', 'github_username', 'work_email', 'personal_emails',
                    'mobile_phone', 'industry', 'job_title', 'job_title_role',
                    'job_title_sub_role', 'job_title_levels', 'job_company_id',
                    'job_company_name', 'job_company_website', 'job_company_industry',
                    'job_company_linkedin_url', 'job_company_linkedin_id',
                    'job_company_facebook_url', 'job_company_twitter_url',
                    'job_company_location_name', 'job_company_location_locality',
                    'job_company_location_metro', 'job_company_location_region',
                    'job_company_location_geo', 'job_company_location_street_address',
                    'job_company_location_address_line_2',
                    'job_company_location_postal_code', 'job_company_location_country',
                    'job_company_location_continent',
                    'location_name', 'location_locality', 'location_metro',
                    'location_region', 'location_country', 'location_continent',
                    'location_street_address', 'location_address_line_2',
                    'location_postal_code', 'location_geo',
                    'phone_numbers', 'emails', 'interests', 'skills', 'location_names',
                    'regions', 'countries', 'street_addresses', 'experience', 'education',
                    'profiles', 'version_status']


def print_list_distances(dict):
    for key in dict.keys():
        for key2 in dict[key]:
            print('{:<s} -> {:<25s} = {:<8f}'.format(key,
                  key2, dict[key][key2]))


def print_all(distances):
    for key in distances.keys():
        for item in distances[key]:
            print(f"{key}->{item}\n")


def log(val):
    location = inspect.stack()[1][3]
    if location not in records:
        records[location] = []

    records[location].append(val)
    return val


def isNaN(num):
    return num != num


class DistCalculation:
    data_keys = ['id', 'full_name', 'first_name', 'middle_initial', 'middle_name',
                 'last_initial', 'last_name', 'gender', 'birth_year', 'birth_date',
                 'linkedin_url', 'linkedin_username', 'linkedin_id', 'facebook_url',
                 'facebook_username', 'facebook_id', 'twitter_url', 'twitter_username',
                 'github_url', 'github_username', 'work_email', 'personal_emails',
                 'mobile_phone', 'industry', 'job_title', 'job_title_role',
                 'job_title_sub_role', 'job_title_levels', 'job_company_id',
                 'job_company_name', 'job_company_website', 'job_company_size',
                 'job_company_founded', 'job_company_industry',
                 'job_company_linkedin_url', 'job_company_linkedin_id',
                 'job_company_facebook_url', 'job_company_twitter_url',
                 'job_company_location_name', 'job_company_location_locality',
                 'job_company_location_metro', 'job_company_location_region',
                 'job_company_location_geo', 'job_company_location_street_address',
                 'job_company_location_address_line_2',
                 'job_company_location_postal_code', 'job_company_location_country',
                 'job_company_location_continent', 'job_last_updated', 'job_start_date',
                 'location_name', 'location_locality', 'location_metro',
                 'location_region', 'location_country', 'location_continent',
                 'location_street_address', 'location_address_line_2',
                 'location_postal_code', 'location_geo', 'location_last_updated',
                 'phone_numbers', 'emails', 'interests', 'skills', 'location_names',
                 'regions', 'countries', 'street_addresses', 'experience', 'education',
                 'profiles', 'version_status']

    list_attributes = ['interests', 'phone_numbers', 'skills', 'location_names',
                       'personal_emails',  'countries',  'job_title_levels', 'regions']

    list_object_attributes = ['emails',  'profiles',
                              'education', 'street_addresses', 'experience', "version_status"]

    def __init__(self):
        self.data_frequencies = dict.fromkeys(self.data_keys, None)

        df_list = []
        for name in glob.glob(f'{os.getcwd()}/dataTool/data/*'):
            df_list.append(pd.read_json(name))

        self.df = pd.concat(df_list)

        # self.df = pd.read_json('./dataTool/data/AppleEmployes.json')
        # self.df = pd.read_json('./dataTool/data/test.json')

        self.df.drop(['version_status'], axis=1, inplace=True)

        self.calc_frequencies()

    def calc_distance_by_instance(self, new_instance):
        """calc the distance between two attributes based on eq3 of mixed data clustering algo """
        pass

    def helper(self, minimum, val1, val2):
        return (abs(val1 - val2) + minimum) / max(val1, val2)

    def calc_distance_for_lists(self, attribute, list1, list2):
        frequencies, total_amount = self.calc_list_frequencies(attribute)
        distances = {}
        minimum = min(frequencies.values())

        for l1 in list1:
            tmp = {}
            for l2 in list2:
                tmp[l2] = self.helper(
                    minimum, frequencies[l1], frequencies[l2])

            distances[l1] = tmp

        print_list_distances(distances)

    def calc_list_frequencies(self, key):
        """
            this function is used to calculate the frequency of a value in a list in our data.
            return val:
                frequencies-  {att1:amount, att2:amount ....}, dictionary of key to instance amount
                total_amount- sum of all amounts in this column => |D|

                TODO: change to numpy/pandas df for efficency
        """
        frequencies = {}
        total_amount = 0

        for items in self.df[key]:
            if type(items) is not list:
                continue

            total_amount += len(items)

            for item in items:
                if item not in frequencies.keys():
                    frequencies[item] = 1
                else:
                    frequencies[item] += 1

        return frequencies,  total_amount

    def calc_frequencies(self):
        """
            driver function for generating frequencies vector.
            for each type of field a different method is invoked.

            ATTENTION - when calculating frequencies for "plain" lists, accessing the data is different
        """

        for key in self.df.keys():
            if key in self.list_object_attributes:
                print(f"in object - type: {key}.\n")
                # TODO need to decide in which way we want to deal with lists / nested objects
                continue

            if key in self.list_attributes:
                # will return a dictionery with 'frequencies' , and 'total_amount' as keys.
                continue
                self.data_frequencies[key] = self.calc_list_frequencies(key)
            else:
                self.data_frequencies[key] = self.df[key].value_counts()

    def eq2(self, size):
        if size <= 3:
            return log(1)
        if size > 3 and size <= 10:
            return log((1 - 0.05 * (size - 3)))
        else:
            return log((0.65 - 0.01 * (size - 10)))

    def valid_input(self, val1, val2, check_for_nan=False):
        if val1 is None:
            return False

        if val2 is None:
            return False

        if check_for_nan:
            if isNaN(val1) or isNaN(val2):
                return False

        return True

    def eq3(self, attribute, val1, val2):
        """calc the distance between two attributes based on eq3 of mixed data clustering algo """
        if not self.valid_input(val1, val2, True):
            return 1

        min_freq = self.data_frequencies[attribute].min()
        v1_freq = self.data_frequencies[attribute][val1]
        v2_freq = self.data_frequencies[attribute][val2]
        max_curr_freq = max(v1_freq, v2_freq)
        dist = (abs(v1_freq - v2_freq) + min_freq) / max_curr_freq

        log(dist)
        return dist

    def eq10(self, attribute, val1, val2, size):
        # print(f"** first: {val1}, second: {val2} **")
        return log(max(self.eq2(size), self.eq3(attribute, val1, val2), THRESHOLD))

    def eq11(self, inst1, inst2):
        sum = 0
        for attribute in categorical_data:
            # skip attributes of lists and objects
            if attribute in self.list_object_attributes or attribute in self.list_attributes:
                continue

            if not self.valid_input(inst1[attribute], inst2[attribute]):
                continue

            if inst1[attribute] == inst2[attribute]:
                continue

            sum += (self.eq10(attribute,
                    inst1[attribute], inst2[attribute], self.df[attribute].nunique())) ** 2

        log(sum)
        return sum

    def eq13(self, inst1, inst2):
        sum = 0
        for attribute in numeric_data:
            # skip attributes of lists and objects
            if attribute in self.list_object_attributes or attribute in self.list_attributes:
                continue

            if not self.valid_input(inst1[attribute], inst2[attribute]):
                continue

            sum += ((inst1[attribute] - inst2[attribute]) ** 2)

        log(sum)
        return sum

    def eq14(self, inst1, inst2):
        return log(math.sqrt(self.eq13(inst1, inst2) + self.eq11(inst1, inst2)))

    def run(self):
        self.distances = {}
        for i in self.df.iterrows():
            tmp = []
            for j in self.df.iterrows():
                tmp.append((
                    j[1]["full_name"], self.eq14(i[1], j[1])))

            self.distances[i[1]["full_name"]] = tmp


if __name__ == '__main__':

    start = time.time()

    x = DistCalculation()

    x.run()

    print(f"done in {time.time() - start}")
    with open('filename.txt', 'w') as f:
        sys.stdout = f
        print_all(x.distances)

    # for record in records.keys():
    #     print(f"{record}:")
    #     print(records[record], "\n")
