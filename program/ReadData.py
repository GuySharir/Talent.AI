import os
import json
import pandas as pd

MIN_FREQ = 1
NUMERIC_DEFAULT = None

# indicated missing raw information -> not included in the hamming distance calculation
HAMMING_DEFAULT = '$'
ONE_HOT_SPARE = 10

DATA_TYPE_PER_INDEX = {0: str, 1: str, 2: str, 3: str,
                       4: int, 5: str, 6: str, 7: str,
                       8: str, 9: str, 10: list, 11: str,
                       12: str, 13: str, 14: list, 15: list,
                       16: dict, 17: dict}

ATTRIBUTE_PER_INDEX = {0: "full_name", 1: "first_name", 2: "last_name", 3: "gender",
                       4: "birth_year", 5: "birth_date", 6: "industry", 7: "job_title",
                       8: "job_title_role", 9: "job_title_sub_role", 10: "job_title_levels",
                       11: "job_company_id", 12: "job_company_name", 13: "job_start_date",
                       14: "interests", 15: "skills",
                       16: "experience", 17: "education"}

# index 16
DATA_TYPE_PER_INDEX_EXPERIENCE = {0: str, 1: str, 2: str, 3: int,
                                  4: str, 5: str, 6: str, 7: bool,
                                  8: str, 9: str, 10: str, 11: str,
                                  12: str, 13: list}

EXPERIENCE_ATTRIBUTE_PER_INDEX = {0: "company_name", 1: "company_size", 2: "company_id", 3: "company_founded",
                                  4: "company_industry", 5: "end_date", 6: "start_date", 7: "current_job",
                                  8: "company_location_name", 9: "company_location_country",
                                  10: "company_location_continent",
                                  11: "title_name", 12: "title_role", 13: "title_levels"}

# index 17
DATA_TYPE_PER_INDEX_EDUCATION = {0: str, 1: str, 2: str, 3: str,
                                 4: float, 5: list, 6: list, 7: list}

EDUCATION_ATTRIBUTE_PER_INDEX = {0: "school_name", 1: "school_type", 2: "end_date", 3: "start_date",
                                 4: "gpa", 5: "degrees", 6: "majors", 7: "minors"}

EXPERIENCE_OBJECT_ATTR_LENGTH = 14
EDUCATION_OBJECT_ATTR_LENGTH = 8


def logger(*args):
    # print(*args)
    pass


def set_path(name) -> str:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{name}'))
    return path


def read_local_json_employees() -> pd.DataFrame:
    path = set_path('dataTool/clean_data')
    all_files = [os.path.join(path, 'AppleEmployees.json'),
                 os.path.join(path, 'AmazonEmployees.json'),
                 # os.path.join(path, 'AdobeEmployees.json'),
                 # os.path.join(path, 'FacebookEmployees.json'),
                 # os.path.join(path, 'TwitterEmployees.json'),
                 # os.path.join(path, 'TeslaEmployees.json'),
                 # os.path.join(path, 'GoogleEmployees.json'),
                 # os.path.join(path, 'IbmEmployees.json'),
                 # os.path.join(path, 'MicrosoftEmployees.json'),
                 # os.path.join(path, 'NvidiaEmployees.json'),
                 # os.path.join(path, 'OracleEmployees.json'),
                 # os.path.join(path, 'SalesforceEmployees.json'),
                 # os.path.join(path, 'UberEmployees.json')
                 ]
    # all_files = [os.path.join(path, 'TwitterEmployees.json'),
    #              os.path.join(path, 'TeslaEmployees.json')]
    li = []
    for filename in all_files:
        with open(filename) as f:
            df = pd.read_json(f)
            li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    # df = df.sample(n=30)
    # logger(f'data from local json- \n{df}')

    return df


def read_freq_per_value_data() -> dict:
    path = set_path('dataTool/frequencies')
    frequencies_path = os.path.abspath(os.path.join(path, 'attributes_frequency.json'))
    with open(frequencies_path) as fp:
        freq = json.load(fp)

    # logger(f'frequencies- \n{freq}')
    return freq


def read_domain_per_attr_data() -> dict:
    path = set_path('dataTool/domain_size')
    domain_path = os.path.abspath(os.path.join(path, 'attributes_domain_size.json'))
    with open(domain_path) as fp:
        domain = json.load(fp)

    # logger(f'domain- \n{domain}')
    return domain


def read_attr_types_data() -> dict:
    path = set_path('dataTool/attributes_types')
    type_path = os.path.abspath(os.path.join(path, 'attributes_types.json'))
    with open(type_path) as f:
        attr_types = json.load(f)
    return attr_types


def read_nested_attr_types_data() -> dict:
    path = set_path('dataTool/attributes_types')
    nested_type_path = os.path.abspath(os.path.join(path, 'nested_attributes_types.json'))
    with open(nested_type_path) as f:
        nested_attr_types = json.load(f)
    return nested_attr_types


if __name__ == '__main__':
    read_local_json_employees()
    read_freq_per_value_data()
    read_domain_per_attr_data()
