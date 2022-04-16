
import requests
import json
# import pandas as pd


# THIS IS MY PAID API TOKEN. MAKE SURE NOT TO UPLOAD IT TO GITHUB OR SOMTHING
API_KEY = "0800ef5dcfb336887e8367b78d1e7eb1694bcfc725463b43cf07b225b6627ed8"

PDL_URL = "https://api.peopledatalabs.com/v5/person/search"

H = {"Content-Type": "application/json", "X-api-key": API_KEY}


#						READ THIS!!

# this is a foramt of elastic search, reaad about it online prior to queying.
# baisiclly you just need to change the compny name to desierd one from our companyes fetched allready.
#

ES_QUERY = {
    "query": {
        "bool": {
            "must_not": [
                {"term": {"full_name": "laura gao"}},
                {"term": {"full_name": "bruk argaw"}},
                {"term": {"full_name": "benson khau"}},
                {"term": {"full_name": "babatunde fashola"}},
                {"term": {"full_name": "sean chan"}},
                {"term": {"full_name": "anurag awasthi"}},
                {"term": {"full_name": "james kelm"}},
                {"term": {"full_name": "reid mckenzie"}},
                {"term": {"full_name": "gregory taylor"}},
                {"term": {"full_name": "kevin rohrbaugh"}},
                {"term": {"full_name": "sambit mishra"}},
                {"term": {"full_name": "raimo tuisku"}},
                {"term": {"full_name": "christopher burnor"}},
                {"term": {"full_name": "uddipan mukherjee"}},
                {"term": {"full_name": "andrew broz"}},
                {"term": {"full_name": "dan haggerty"}},
                {"term": {"full_name": "chris schenk"}},
                {"term": {"full_name": "joey carmello"}},
                {"term": {"full_name": "andrew rapp"}},
                {"term": {"full_name": "william blasko"}},
                {"term": {"full_name": "david marwick"}},
                {"term": {"full_name": "charlie croom"}},
                {"term": {"full_name": "laurențiu dascălu"}},
                {"term": {"full_name": "matt gadda"}},
                {"term": {"full_name": "brian wickman"}},
                {"term": {"full_name": "linds panther"}},
                {"term": {"full_name": "brian kahrs"}},
                {"term": {"full_name": "joshua perline"}},
                {"term": {"full_name": "scott nelson"}},
                {"term": {"full_name": "kevin shieh"}},
                {"term": {"full_name": "sam toizer"}},
                {"term": {"full_name": "leah culver"}},
                {"term": {"full_name": "gary zhang"}},
                {"term": {"full_name": "babatunde fashola"}},
                {"term": {"full_name": "sean chan"}},
                {"term": {"full_name": "anurag awasthi"}},
                {"term": {"full_name": "james kelm"}},
                {"term": {"full_name": "reid mckenzie"}},
                {"term": {"full_name": "gregory taylor"}},
                {"term": {"full_name": "james bellenger"}},
                {"term": {"full_name": "kevin rohrbaugh"}},
                {"term": {"full_name": "raimo tuisku"}},
                {"term": {"full_name": "christopher burnor"}},
                {"term": {"full_name": "andrew broz"}},
                {"term": {"full_name": "dan haggerty"}},
                {"term": {"full_name": "shatil rafiullah"}},
                {"term": {"full_name": "chris schenk"}},
                {"term": {"full_name": "joey carmello"}},
                {"term": {"full_name": "kostas pagratis"}},
                {"term": {"full_name": "brent halsey"}},
                {"term": {"full_name": "william blasko"}},
                {"term": {"full_name": "ryan guthrie"}},
                {"term": {"full_name": "charlie croom"}},
                {"term": {"full_name": "anton panasenko"}},
                {"term": {"full_name": "sidharth shanker"}},
                {"term": {"full_name": "anne gatchell"}},
                {"term": {"full_name": "vladimir chernis"}},
                {"term": {"full_name": "lisa white"}},
                {"term": {"full_name": "david bernadett"}},
                {"term": {"full_name": "benson khau"}},
                {"term": {"full_name": "william love"}},
            ],
            "must": [
                {"term": {"job_company_name": "twitter"}},
                {"term": {"location_country": "united states"}},
                {"term": {"industry": "computer software"}},

                {"exists": {"field": "gender"}},
                {"exists": {"field": "linkedin_username"}},
                # {"term": {"industry": "internet"}},
                {"exists": {"field": "birth_year"}},
                # {"exists": {"field": "birth_date"}},
                # {"exists": {"field": "linkedin_url"}},
                # {"exists": {"field": "linkedin_id"}},
                {"exists": {"field": "facebook_url"}},
                {"exists": {"field": "facebook_username"}},
                # {"exists": {"field": "facebook_id"}},
                # {"exists": {"field": "twitter_url"}},
                # {"exists": {"field": "twitter_username"}},
                # {"exists": {"field": "github_url"}},
                # {"exists": {"field": "github_username"}},
                {"exists": {"field": "personal_emails"}},
                # {"exists": {"field": "work_email"}},
                # {"exists": {"field": "mobile_phone"}},
                # {"exists": {"field": "job_title_levels"}},
                # {"exists": {"field": "phone_numbers"}},
                {"exists": {"field": "industry"}},
                {"exists": {"field": "job_title"}},
                {"exists": {"field": "job_title_role"}},
                {"exists": {"field": "job_title_sub_role"}},
                {"exists": {"field": "job_company_industry"}},
                {"exists": {"field": "job_company_location_locality"}},
                {"exists": {"field": "job_company_location_region"}},
                {"exists": {"field": "job_last_updated"}},
                {"exists": {"field": "job_start_date"}},
                {"exists": {"field": "emails"}},
                {"exists": {"field": "interests"}},
                {"exists": {"field": "skills"}},
                {"exists": {"field": "location_names"}},
                {"exists": {"field": "regions"}},
                {"exists": {"field": "countries"}},
                # {"exists": {"field": "street_addresses"}},
                # {"exists": {"field": "street_addresses.street_address"}},
                # {"exists": {"field": "street_addresses.name"}},
                # {"exists": {"field": "street_addresses.region"}},
                # {"exists": {"field": "street_addresses.continent"}},
                # {"exists": {"field": "experience"}},
                # {"exists": {"field": "experience.title.levels"}},
                # {"exists": {"field": "experience.title.sub_role"}},
                # {"exists": {"field": "experience.company.website"}},
                {"exists": {"field": "experience.title"}},
                {"exists": {"field": "experience.title.name"}},
                {"exists": {"field": "experience.title.role"}},
                {"exists": {"field": "experience.company"}},
                {"exists": {"field": "experience.company.name"}},
                {"exists": {"field": "experience.company.founded"}},
                {"exists": {"field": "experience.company.size"}},
                {"exists": {"field": "experience.company.industry"}},
                # {"exists": {"field": "experience.company.linkedin_url"}},
                # {"exists": {"field": "experience.company.facebook_url"}},
                # {"exists": {"field": "experience.company.twitter_url"}},
                # {"exists": {"field": "experience.location_names"}},
                {"exists": {"field": "experience.start_date"}},
                {"exists": {"field": "experience.end_date"}},
                {"exists": {"field": "experience.title.name"}},
                {"exists": {"field": "experience.is_primary"}},
                {"exists": {"field": "experience.company.location"}},
                {"exists": {"field": "education.degrees"}},
                {"exists": {"field": "education.majors"}},
                # {"exists": {"field": "education"}},
                # {"exists": {"field": "education.minors"}},
                # {"exists": {"field": "education.school"}},
                # {"exists": {"field": "education.school.website"}},
                # {"exists": {"field": "education.school.location.name"}},
                {"exists": {"field": "education.school.name"}},
                {"exists": {"field": "education.school.type"}},
                {"exists": {"field": "education.school.location"}},
                # {"exists": {"field": "education.gpa"}},
                {"exists": {"field": "education.start_date"}},
                {"exists": {"field": "education.end_date"}},
                # {"exists": {"field": "profiles"}},
                # {"exists": {"field": "profiles.url"}},
                # {"exists": {"field": "profiles.network"}},
                # {"exists": {"field": "profiles.username"}},
                # {"exists": {"field": "version_status.status"}},
                {"exists": {"field": "version_status.current_version"}},
                {"exists": {"field": "version_status.previous_version"}},
            ]
        }
    }
}

# **************    BEWARE OF SIZE! WE DO NOT WANT TO EXCEED OUR LIMIT ************
# 					QUERY WITH CAUTION, MAKE SURE AL PARAMS ARE CORRECT


P = {"query": json.dumps(ES_QUERY), "size": 13, "pretty": True}


# this function will add peapole to the file "employes.json right after the current entries
def write_json(new_data,):
    with open("TwitterEmployees.json", 'r+') as file:
        file_data = json.load(file)
        file_data["employes"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


response = requests.get(PDL_URL, headers=H, params=P).json()

if response["status"] == 200:
    data = response["data"]
    print(f"successfully grabbed {len(data)} records from pdl")
    print(f"{response['total']} total pdl records exist matching this query")

    for record in data:
        write_json(record)

else:
    print(
        "NOTE. The carrier pigeons lost motivation in flight. See error and try again."
    )
    print("Error:", response)
