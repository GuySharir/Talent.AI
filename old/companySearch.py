import requests
import json
API_KEY = '0800ef5dcfb336887e8367b78d1e7eb1694bcfc725463b43cf07b225b6627ed8'

PDL_URL = "https://api.peopledatalabs.com/v5/company/search"

H = {
    'Content-Type': "application/json",
    'X-api-key': API_KEY
}

ES_QUERY = {
    "query": {
        "bool": {
            "must": [
                {"term": {"website": "salesforce.com"}},
            ]
        }
    }
}

P = {
    'query': json.dumps(ES_QUERY),
    'size': 1,
    'pretty': True
}


def write_json(new_data,):
    with open("../dataTool/companys.json", 'r+') as file:
        file_data = json.load(file)
        file_data["company"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


response = requests.get(
    PDL_URL,
    headers=H,
    params=P
).json()

if response["status"] == 200:
    data = response['data']

    for record in data:
        write_json(record)

    print(f"successfully grabbed {len(data)} records from pdl")
    print(f"{response['total']} total pdl records exist matching this query")
else:
    print("NOTE. The carrier pigeons lost motivation in flight. See error and try again.")
    print("Error:", response)
