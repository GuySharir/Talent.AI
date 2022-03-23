from pydoc import locate
import pandas as pd
from programFlow.ReadData import read_local_json_employees, read_attr_types_data, read_freq_per_value_data
import numpy as np


def logger(*args):
    # print(*args)
    pass


def df_row_to_instance(df: pd.DataFrame, index: int) -> dict:
    attr_types = read_attr_types_data()
    return {attr: df.iloc[index][inx] for inx, attr in enumerate(attr_types.keys())}


def convert_to_freq(val_type, freq_val, val, instance_freq_vec) -> list:
    if val_type == str:
        if not val:
            val = 'null'
        instance_freq_vec.append(freq_val[val])

    elif val_type == float or val_type == int:
        instance_freq_vec.append(val)

    return instance_freq_vec


def convert_instance_to_freq_vec(instance: dict) -> dict:
    logger(f'instance raw data- \n{instance}')

    freq = read_freq_per_value_data()
    attr_types = read_attr_types_data()

    instance_freq_vec = []
    name = instance["full_name"]

    for attr, val in instance.items():
        val_type = locate(attr_types[attr].split("'")[1])
        freq_val = freq[attr]

        if val_type == float or val_type == int or val_type == str:
            instance_freq_vec = convert_to_freq(val_type=val_type, freq_val=freq_val,
                                                val=val, instance_freq_vec=instance_freq_vec)
        # elif val_type == list:
        #     for list_val in val:
        #         instance_freq_vec = convert_to_freq(val_type=val_type, freq_val=freq_val,
        #                                             val=list_val, instance_freq_vec=instance_freq_vec)

    result = {name: instance_freq_vec}
    logger(f'instance as frequencies vector- \n{result}')
    return result


def loop_candidates_convert_to_freq_vec():
    df = read_local_json_employees()

    converted = []

    for row in range(0, len(df)):
        # for row in range(0, 2):
        instance = df_row_to_instance(df=df, index=row)
        instance_freq_vec = convert_instance_to_freq_vec(instance=instance)
        converted.append(instance_freq_vec)

    return converted


if __name__ == '__main__':
    x = loop_candidates_convert_to_freq_vec()
    from sklearn.cluster import KMeans
