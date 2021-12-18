import numpy as np
import pandas as pd
import os


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
    list_attributes = ['interests', 'emails', 'phone_numbers', 'skills', 'location_names', 'profiles',
                       'personal_emails', 'education', 'street_addresses', 'countries', 'experience', 'job_title_levels', 'regions']

    def __init__(self, data_path):
        self.data_frequencies = dict.fromkeys(self.data_keys, None)

        # TODO need to be extended for each file in the dataset and not a specific file
        with open(data_path) as data_file:
            self.df = pd.read_json(data_file)

    def calc_frequencies(self):
        for key in self.data_keys:
            if key in self.list_attributes:
                # TODO need to decide in which way we want to deal with lists / nested objects
                continue

            self.data_frequencies[key] = self.df[key].value_counts()

        # for key in self.data_frequencies:
        #     print(f"{self.data_frequencies[key]}\n")


if __name__ == '__main__':
    x = DistCalculation('./dataTool/data/AppleEmployes.json')
    x.calc_frequencies()
