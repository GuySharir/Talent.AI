import requests
import json
import pandas as pd


json_file = pd.read_json('my_pdl_search.json')

json_file.to_csv('companys.csv', index=None)
