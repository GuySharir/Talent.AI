from typing import List
import pandas as pd
import glob
import os


def print_list_distances(dict):
    for key in dict.keys():
        for key2 in dict[key]:
            print('{:<s} -> {:<25s} = {:<8f}'.format(key,
                  key2, dict[key][key2]))


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
                              'education', 'street_addresses' 'experience']

    def __init__(self):
        self.data_frequencies = dict.fromkeys(self.data_keys, None)

        df_list = []
        for name in glob.glob(f'{os.getcwd()}/dataTool/data/*'):
            print(name)
            df_list.append(pd.read_json(name))

        self.df = pd.concat(df_list)
        self.df.drop(['version_status', "company"], axis=1, inplace=True)

        # self.calc_frequencies()

    def calc_distance_by_attribute(self, attribute, val1, val2):
        """calc the distance between two attributes based on eq3 of mixed data clustering algo """

        min_freq = self.data_frequencies[attribute].min()
        v1_freq = self.data_frequencies[attribute][val1]
        v2_freq = self.data_frequencies[attribute][val2]
        max_curr_freq = max(v1_freq, v2_freq)
        dist = (abs(v1_freq - v2_freq) + min_freq) / max_curr_freq

        return dist

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

        for key in self.data_keys:
            if key in self.list_object_attributes:
                print(f"in object - type: {key}.\n")
                # TODO need to decide in which way we want to deal with lists / nested objects
                continue

            if key in self.list_attributes:
                # will return a dictionery with 'frequencies' , and 'total_amount' as keys.
                self.data_frequencies[key] = self.calc_list_frequencies(key)
            else:
                self.data_frequencies[key] = self.df[key].value_counts()


if __name__ == '__main__':
    x = DistCalculation()
    print("****************************************")
    a = [
        "java",
        "c++",
        "c",
        "windows",
        "sql",
        "javascript",
        "html",
        "linux",
        "oracle",
        "python",
        "sql db2",
        "uml",
        "salesforce.com",
        "mongodb",
        "nosql",
        "db2",
        "tcp/ip",
        "udp",
        "dns",
        "coldfusion",
        "docker",
        "jquery mobile",
        "bootstrap",
        "bamboo",
        "ruby",
        "ftp",
        "scp",
        "https",
        "ieee 802.11",
        "lte"
    ]

    b = [
        "java",
        "c++",
        "c#",
        "xml",
        "xcode",
        "perl",
        "objective c",
        "j2ee",
        "javascript",
        "c",
        "subversion",
        "ajax",
        "sql",
        "mysql",
        "linux",
        "html",
        "apache",
        "iphone",
        "jquery",
        "php",
        "databases",
        "integration",
        "java enterprise edition",
        "mobile applications",
        "web applications",
        "ios"
    ]
    x.calc_distance_for_lists("skills", a, b)

    # for name in glob.glob(f'{os.getcwd()}/dataTool/data/*'):
    #     print(name)

    # print(x.data_frequencies, '\n')
    # print(x.calc_list_freq("skills"))
    # x.calc_list_freq("skills")

    # print(x.data_frequencies["skills"])

    # x.calc_distance("job_title", "senior software engineer",
    #                 "software engineer")
