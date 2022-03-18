from typing import List
from numpy import NaN, nan
import pandas as pd
import glob
import os
import sys
import math
import inspect
import time
import json

result = {}


def print_all(distances):
    for key in distances.keys():
        print(f"{key.split('/')[-1]}->{distances[key]}\n")


for name in glob.glob(f'{os.getcwd()}/dataTool/data/*'):
    with open(name, 'r') as file:
        file_data = json.load(file)
        result[name] = len(file_data)


print_all(result)
