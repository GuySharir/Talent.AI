from pydoc import locate

import numpy as np
import pandas as pd

from program.PeriodicalDomainFreq import DomainFreqCalc
from program.ReadData import read_local_json_employees, read_attr_types_data, read_nested_attr_types_data, \
    read_freq_per_value_data, MIN_FREQ, NUMERIC_DEFAULT, HAMMING_DEFAULT, ONE_HOT_SPARE, set_path
from dataTool.runtimeObjectsInfo.ListLengthData import LIST_LENGTH_PER_ATTR, NESTED_LENGTH_PER_ATTR
from DistEnum import DistMethod, DefaultVal


def logger(*args):
    print(*args)
    # pass


def df_row_to_instance(df: pd.DataFrame, index: int) -> dict:
    attr_types = read_attr_types_data()
    return {attr: df.iloc[index][inx] for inx, attr in enumerate(attr_types.keys())}


def convert_to_freq_categorical(val_type, freq_val: dict, val, instance_freq_vec: list) -> list:
    if val == DefaultVal.Nested_default:
        instance_freq_vec.append(MIN_FREQ)

    else:
        if val_type == str and not val:
            val = 'null'
        elif val_type == bool and not val:
            val = 'false'
        elif val_type == bool and val:
            val = 'true'
        if val not in freq_val.keys():
            instance_freq_vec.append(MIN_FREQ)
        else:
            instance_freq_vec.append(freq_val[val])
    return instance_freq_vec


def convert_to_freq_numerical(val, instance_freq_vec) -> list:
    if val == DefaultVal.Nested_default:
        instance_freq_vec.append(NUMERIC_DEFAULT)
    else:
        instance_freq_vec.append(val)

    return instance_freq_vec


def list_to_vec_representation(representation_option: DistMethod, attr_name: str, freq_val: dict, list_val: list, instance_freq_vec: list) -> list:
    # each list contains only categorical values
    # logger(f'########################################## list ######################################')
    logger(f'attr-\n{attr_name}')
    # logger(f'list val-\n{list_val}')
    # logger(f'attr average length-\n{LIST_LENGTH_PER_ATTR[attr_name]}')
    # logger(f'list representation option-\n{representation_option}')
    # logger(f'vec before list conversion-\n{instance_freq_vec}')

    if representation_option == DistMethod.fix_length_freq:
        attr_length = LIST_LENGTH_PER_ATTR[attr_name]
        freq_values_representation = []

        if not list_val:
            freq_values_representation = [MIN_FREQ] * attr_length
            instance_freq_vec.extend(freq_values_representation)
        else:
            if len(list_val) < attr_length:
                length_gap = attr_length - len(list_val)
                for val in list_val:
                    freq_values_representation = convert_to_freq_categorical(val_type=str, freq_val=freq_val, val=val, instance_freq_vec=freq_values_representation)
                freq_values_representation.extend([MIN_FREQ] * length_gap)
            else:
                for val in list_val[:attr_length]:
                    freq_values_representation = convert_to_freq_categorical(val_type=str, freq_val=freq_val, val=val, instance_freq_vec=freq_values_representation)
            freq_values_representation.sort(reverse=True)
            instance_freq_vec.extend(freq_values_representation)

        logger(f'freq list conversion- \n{freq_values_representation}')
        logger(f'freq list conversion len = {len(freq_values_representation)}')
        # logger(f'vec after list conversion- \n{instance_freq_vec}')

    elif representation_option == DistMethod.inner_product or representation_option == DistMethod.intersection:
        # logger(f'freq val-\n{freq_val}')
        one_hot_values_representation = [1 if value in list_val else 0 for value in freq_val.keys()]
        # one hot vector spare extension for future list values
        one_hot_values_representation.extend([0] * ONE_HOT_SPARE)
        instance_freq_vec.extend(one_hot_values_representation)
        # logger(f'one hot values representation-\n{one_hot_values_representation}')

    elif representation_option == DistMethod.hamming_distance:
        attr_length = LIST_LENGTH_PER_ATTR[attr_name]
        hamming_values_representation = []
        if not list_val:
            hamming_values_representation = [HAMMING_DEFAULT] * attr_length
            instance_freq_vec.extend(hamming_values_representation)
        else:
            if len(list_val) < attr_length:
                length_gap = attr_length - len(list_val)
                for val in list_val:
                    hamming_values_representation.append(val)
                hamming_values_representation.extend([HAMMING_DEFAULT] * length_gap)
            else:
                for val in list_val[:attr_length]:
                    hamming_values_representation.append(val)
            instance_freq_vec.extend(hamming_values_representation)
        logger(f'freq list conversion- \n{hamming_values_representation}')
        logger(f'freq list conversion len = {len(hamming_values_representation)}')
    logger(f'########################################################################################')
    return instance_freq_vec


def create_default_empty_list_for_nested_attr(nested_attr: dict, representation_option_nested: DistMethod, representation_option_set: DistMethod, attr_name: str, freq_val: dict) -> list:
    freq_values_per_object = []
    for attr, attr_type in nested_attr[attr_name].items():
        attr_type = locate(attr_type.split("'")[1])
        if attr_type == list:
            list_to_vec_representation(representation_option=representation_option_set, attr_name=attr,
                                       freq_val=freq_val[attr],
                                       list_val=[], instance_freq_vec=freq_values_per_object)
        elif attr_type == float or attr_type == int:
            if representation_option_nested == DistMethod.hamming_distance:
                freq_values_per_object.append(HAMMING_DEFAULT)
            else:
                freq_values_per_object = convert_to_freq_numerical(val=DefaultVal.Nested_default,
                                                                   instance_freq_vec=freq_values_per_object)
        else:
            if representation_option_nested == DistMethod.hamming_distance:
                freq_values_per_object.append(HAMMING_DEFAULT)
            else:
                freq_values_per_object = convert_to_freq_categorical(val_type=attr_type, freq_val=freq_val[attr], val=DefaultVal.Nested_default,
                                                                     instance_freq_vec=freq_values_per_object)

        # logger(f' default freq_values_per_object-\n {freq_values_per_object}')

    return freq_values_per_object


def create_single_obj_list_for_nested_attr(nested_attr: dict, representation_option_nested: DistMethod, representation_option_set: DistMethod, attr_name: str, freq_val: dict, nested_obj: dict) -> list:
    freq_values_per_object = []
    for attr, val in nested_obj.items():
        # logger(f'attribute- {attr}')
        attr_type = nested_attr[attr_name][attr]
        attr_type = locate(attr_type.split("'")[1])

        if attr_type == list:
            list_to_vec_representation(representation_option=representation_option_set, attr_name=attr,
                                       freq_val=freq_val[attr],
                                       list_val=val, instance_freq_vec=freq_values_per_object)
        elif attr_type == float or attr_type == int:
            if representation_option_nested == DistMethod.hamming_distance:
                freq_values_per_object.append(val)
            else:
                freq_values_per_object = convert_to_freq_numerical(val=val, instance_freq_vec=freq_values_per_object)
        else:
            if representation_option_nested == DistMethod.hamming_distance:
                freq_values_per_object.append(val)
            else:
                freq_values_per_object = convert_to_freq_categorical(val_type=attr_type, freq_val=freq_val[attr], val=val,
                                                                     instance_freq_vec=freq_values_per_object)

        # logger(f'freq_values_per_object-\n {freq_values_per_object}')

    return freq_values_per_object


def nested_to_vec_representation(representation_option: DistMethod, representation_option_set: DistMethod, attr_name: str, freq_val: dict, nested_val: dict, instance_freq_vec: list) -> list:
    # logger(f'########################################## nested ######################################3')
    # logger(f'attr-\n{attr_name}')
    # logger(f'nested val-\n{nested_val}')
    # logger(f'attr length-\n{NESTED_LENGTH_PER_ATTR[attr_name]}')
    # logger(f'nested representation option-\n{representation_option}')
    # logger(f'set representation option-\n{representation_option_set}')
    # logger(f'vec before nested conversion-\n{instance_freq_vec}')
    # logger(f'vec before nested conversion len-\n{len(instance_freq_vec)}')

    nested_attr = read_nested_attr_types_data()
    # logger(f'nested_attr {nested_attr[attr_name]}')

    if representation_option == DistMethod.fix_length_freq or representation_option == DistMethod.hamming_distance:
        attr_length = NESTED_LENGTH_PER_ATTR[attr_name]
        freq_values_representation = []

        if not nested_val:
            freq_values_per_object = create_default_empty_list_for_nested_attr(nested_attr=nested_attr,
                                                                               representation_option_nested=representation_option,
                                                                               representation_option_set=representation_option_set,
                                                                               attr_name=attr_name, freq_val=freq_val)
            freq_values_representation.extend(freq_values_per_object * attr_length)

        else:
            if len(nested_val) < attr_length:
                # logger(f'attr len - {len(nested_val)}')
                length_gap = attr_length - len(nested_val)
                for nested_obj in nested_val:
                    freq_values_per_object = create_single_obj_list_for_nested_attr(nested_attr=nested_attr,
                                                                                    representation_option_nested=representation_option,
                                                                                    representation_option_set=representation_option_set,
                                                                                    attr_name=attr_name,
                                                                                    freq_val=freq_val, nested_obj=nested_obj)
                    freq_values_representation.extend(freq_values_per_object)
                freq_values_per_object = create_default_empty_list_for_nested_attr(nested_attr=nested_attr,
                                                                                   representation_option_nested=representation_option,
                                                                                   representation_option_set=representation_option_set,
                                                                                   attr_name=attr_name,
                                                                                   freq_val=freq_val)
                freq_values_representation.extend(freq_values_per_object * length_gap)

            else:
                for nested_obj in nested_val[:attr_length]:
                    freq_values_per_object = create_single_obj_list_for_nested_attr(nested_attr=nested_attr,
                                                                                    representation_option_nested=representation_option,
                                                                                    representation_option_set=representation_option_set,
                                                                                    attr_name=attr_name,
                                                                                    freq_val=freq_val, nested_obj=nested_obj)
                    freq_values_representation.extend(freq_values_per_object)

        instance_freq_vec.extend(freq_values_representation)
        # logger(f'freq_values_representation-\n{freq_values_representation}')
        # logger(f'freq_values_representation len-\n{len(freq_values_representation)}')
        #
        # logger(f'instance_freq_vec-\n{instance_freq_vec}')
        # logger(f'instance_freq_vec len-\n{len(instance_freq_vec)}')
    return instance_freq_vec


def convert_instance_to_freq_vec(instance: dict, representation_option: DistMethod, representation_option_set: DistMethod, representation_option_nested: DistMethod) -> dict:
    freq = read_freq_per_value_data()
    attr_types = read_attr_types_data()

    instance_freq_vec = []
    name = instance["full_name"]
    company = instance["job_company_name"]

    for attr, val in instance.items():
        val_type = locate(attr_types[attr].split("'")[1])
        freq_val = freq[attr]

        if val_type == float or val_type == int:
            if representation_option == DistMethod.fix_length_freq:
                instance_freq_vec = convert_to_freq_numerical(val=val, instance_freq_vec=instance_freq_vec)
            elif representation_option == DistMethod.hamming_distance:
                instance_freq_vec.append(val)

        elif val_type == str:
            if representation_option == DistMethod.fix_length_freq:
                instance_freq_vec = convert_to_freq_categorical(val_type=val_type, freq_val=freq_val,
                                                                val=val, instance_freq_vec=instance_freq_vec)
            elif representation_option == DistMethod.hamming_distance:
                instance_freq_vec.append(val)

        elif val_type == list:
            instance_freq_vec = list_to_vec_representation(representation_option=representation_option_set, attr_name=attr, freq_val=freq_val,
                                                           list_val=val, instance_freq_vec=instance_freq_vec)

        elif val_type == dict:
            instance_freq_vec = nested_to_vec_representation(representation_option=representation_option_nested, representation_option_set=representation_option_set,
                                                             attr_name=attr, freq_val=freq_val,
                                                             nested_val=val, instance_freq_vec=instance_freq_vec)

    result = {name: (company, instance_freq_vec)}
    logger(f'vector length- {len(instance_freq_vec)}')
    return result


def loop_candidates_convert_to_freq_vec(df: pd.DataFrame, representation_option: DistMethod, representation_option_for_set: DistMethod, representation_option_for_nested: DistMethod):
    DomainFreqCalc(df=df).calc_domain_freq_per_value()
    df_converted = set_path('dataTool/df_converted.npy')
    result = []
    for row in range(0, len(df)):
        instance = df_row_to_instance(df=df, index=row)
        instance_freq_vec = convert_instance_to_freq_vec(instance=instance, representation_option=representation_option, representation_option_set=representation_option_for_set, representation_option_nested=representation_option_for_nested)
        result.append(instance_freq_vec)
        logger(f'instance as raw data- \n{instance}')
        logger(f'instance as frequencies vector- \n{instance_freq_vec}')
        logger(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    np.save(df_converted, result)


def freq_rep(instance: dict) -> list:
    instance_freq_vec = convert_instance_to_freq_vec(instance=instance, representation_option=DistMethod.fix_length_freq,
                                                     representation_option_set=DistMethod.fix_length_freq,
                                                     representation_option_nested=DistMethod.fix_length_freq)
    logger(f'instance as raw data- \n{instance}')
    logger(f'instance as rep vector- \n{instance_freq_vec}')

    return (list(instance_freq_vec.values())[0])[1]


def hamming_rep(instance: dict) -> list:
    instance_hamming_vec = convert_instance_to_freq_vec(instance=instance, representation_option=DistMethod.hamming_distance,
                                                        representation_option_set=DistMethod.hamming_distance,
                                                        representation_option_nested=DistMethod.hamming_distance)
    logger(f'instance as raw data- \n{instance}')
    logger(f'instance as rep vector- \n{instance_hamming_vec}')
    return (list(instance_hamming_vec.values())[0])[1]


def one_hot_rep(instance: dict) -> list:
    instance_one_hot_vec = convert_instance_to_freq_vec(instance=instance, representation_option=DistMethod.fix_length_freq,
                                                        representation_option_set=DistMethod.inner_product,
                                                        representation_option_nested=DistMethod.fix_length_freq)
    logger(f'instance as raw data- \n{instance}')
    logger(f'instance as rep vector- \n{instance_one_hot_vec}')
    return (list(instance_one_hot_vec.values())[0])[1]


if __name__ == '__main__':
    # loop over df using 4 rep options
    # df_ = read_local_json_employees()
    # hamming
    # loop_candidates_convert_to_freq_vec(df=df_,representation_option=DistMethod.hamming_distance, representation_option_for_set=DistMethod.hamming_distance, representation_option_for_nested=DistMethod.hamming_distance)
    # freq
    # loop_candidates_convert_to_freq_vec(df=df_, representation_option=DistMethod.fix_length_freq, representation_option_for_set=DistMethod.fix_length_freq, representation_option_for_nested=DistMethod.fix_length_freq)
    # one hot intersection
    # loop_candidates_convert_to_freq_vec(df=df_,representation_option=DistMethod.fix_length_freq, representation_option_for_set=DistMethod.intersection, representation_option_for_nested=DistMethod.fix_length_freq)
    # one hot inner_product
    # loop_candidates_convert_to_freq_vec(df=df_,representation_option=DistMethod.fix_length_freq, representation_option_for_set=DistMethod.inner_product, representation_option_for_nested=DistMethod.fix_length_freq)

    # ---------------------------------------------------------------------------------------

    # representation per instance using 4 rep options
    instance_ = {
        "full_name": "laura gao",
        "first_name": "laura",
        "last_name": "gao",
        "gender": "female",
        "birth_year": 1996,
        "birth_date": None,
        "industry": "internet",
        "job_title": "associate product manager ii",
        "job_title_role": "operations",
        "job_title_sub_role": "product",
        "job_title_levels": [],
        "job_company_id": "twitter",
        "job_company_name": "twitter",
        "job_start_date": "2018-09",
        "interests": [
            "potenciamiento econ\u00f3mico"
        ],
        "skills": [
            "public speaking",
            "management",
            "microsoft office",
            "technology",
            "creative strategy",
            "photoshop",
            "visual arts",
            "customer service",
            "data analysis",
            "stock trading",
            "leadership",
            "microsoft excel",
            "product management",
            "powerpoint",
            "product design",
            "fundraising",
            "design"
        ],
        "experience": [
            {
                "company_name": "smartypal",
                "company_size": "1-10",
                "company_id": "smartypal",
                "company_founded": 2013,
                "company_industry": "e-learning",
                "end_date": "2017",
                "start_date": "2017",
                "current_job": False,
                "company_location_name": "philadelphia, pennsylvania, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "product management intern",
                "title_role": "operations",
                "title_levels": [
                    "training"
                ]
            },
            {
                "company_name": "amazon",
                "company_size": "10001+",
                "company_id": "amazon",
                "company_founded": 1994,
                "company_industry": "internet",
                "end_date": "2017-08",
                "start_date": "2017-06",
                "current_job": False,
                "company_location_name": "seattle, washington, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "business data analyst intern",
                "title_role": "engineering",
                "title_levels": [
                    "training"
                ]
            },
            {
                "company_name": "consumer financial protection bureau",
                "company_size": "1001-5000",
                "company_id": "consumer-financial-protection-bureau",
                "company_founded": 2010,
                "company_industry": "government administration",
                "end_date": "2015-08",
                "start_date": "2015-06",
                "current_job": False,
                "company_location_name": "washington, district of columbia, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "chief of staff policy intern",
                "title_role": None,
                "title_levels": [
                    "training"
                ]
            },
            {
                "company_name": "twitter",
                "company_size": "1001-5000",
                "company_id": "twitter",
                "company_founded": 2006,
                "company_industry": "internet",
                "end_date": None,
                "start_date": "2018-09",
                "current_job": True,
                "company_location_name": "san francisco, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "associate product manager ii",
                "title_role": "operations",
                "title_levels": []
            }
        ],
        "education": [
            {
                "school_name": "graduate school of city planning minor",
                "school_type": None,
                "end_date": None,
                "start_date": None,
                "gpa": None,
                "degrees": [
                    "bachelors",
                    "bachelor of science"
                ],
                "majors": [],
                "minors": []
            },
            {
                "school_name": "coppell high school",
                "school_type": "secondary school",
                "end_date": "2014-05",
                "start_date": None,
                "gpa": None,
                "degrees": [],
                "majors": [],
                "minors": []
            },
            {
                "school_name": "the wharton school",
                "school_type": "post-secondary institution",
                "end_date": "2018",
                "start_date": "2014",
                "gpa": 3.64,
                "degrees": [
                    "bachelors",
                    "bachelor of science"
                ],
                "majors": [
                    "economics",
                    "statistics",
                    "finance"
                ],
                "minors": []
            },
            {
                "school_name": "coppell high school",
                "school_type": "secondary school",
                "end_date": "2014",
                "start_date": "2010",
                "gpa": None,
                "degrees": [],
                "majors": [],
                "minors": []
            },
            {
                "school_name": "university of pennsylvania",
                "school_type": "post-secondary institution",
                "end_date": "2018",
                "start_date": "2014",
                "gpa": 3.7,
                "degrees": [
                    "bachelors",
                    "bachelor of science"
                ],
                "majors": [
                    "economics",
                    "statistics",
                    "finance"
                ],
                "minors": []
            }
        ]
    }
    # freq_rep(instance=instance_)
    # hamming_rep(instance=instance_)
    one_hot_rep(instance=instance_)

    a = {
    "full_name": "sivan",
    "first_name": "$",
    "last_name": "$",
    "gender": "$",
    "birth_year": None,
    "birth_date": "$",
    "industry": "Internet",
    "job_title": "business product marketing, program manager",
    "job_title_role": "marketing",
    "job_title_sub_role": "product_marketing",
    "job_title_levels": [
        "Intern"
    ],
    "job_company_id": "facebook",
    "job_company_name": "facebook",
    "job_start_date": "2020-03",
    "interests": [
        "travelling",
        "environment",
        "photography",
        "palmistry",
        "science and technology",
        "sketching",
        "animal welfare",
        "health"
    ],
    "skills": [
        "brand management",
        "strategy",
        "team management",
        "marketing management",
        "marketing",
        "crm",
        "market research",
        "management",
        "product marketing",
        "market analysis",
        "product development",
        "key account management",
        "product management",
        "cross functional team leadership",
        "business development",
        "business strategy",
        "project management",
        "customer relationship management",
        "product launch",
        "start ups",
        "business analysis",
        "negotiation",
        "consumer insight",
        "digital marketing",
        "sales operations",
        "customer insight",
        "social media marketing",
        "saas",
        "software as a service",
        "user experience",
        "user interface",
        "user research"
    ],
    "experience": [],
    "education": [],
}
    # freq_rep(instance=a)
    # hamming_rep(instance=a)
    one_hot_rep(instance=a)
