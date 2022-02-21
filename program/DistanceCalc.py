from algorithems.NumDistance import NumDistance
from program.cleanData import CleanData
import json


class Distance:
    """
        This class (Program) is responsible for the distance calculation
        - self.files, list of json files contains employees data
        - self.fields_list, list of relevant attributes to extract from employees' data
        - clean_data_path, path to a folder where we save all cleaned data
        - data_per_company, a dictionary contains employees data per company
        - attr_type, a dictionary contains the attribute name and the distance result for numerical data


        """
    def __init__(self, instance_a: dict, instance_b: dict):
        self.attr_type = {}
        self.instance_a = instance_a
        self.instance_b = instance_b

    def calc_distance(self):
        self.attr_type = {attribute: type(self.instance_a.get(attribute)) for attribute in self.instance_a.keys()}
        print(self.attr_type)

        for attribute in self.attr_type.keys():
            if self.attr_type[attribute] == int or self.attr_type[attribute] == float:
                print(NumDistance(attribute, self.instance_a[attribute], self.instance_b[attribute]).calc_num_distance())
            elif self.attr_type[attribute] == str:
                print(f'string attr {attribute}')

            elif self.attr_type[attribute] == list:
                if type(self.instance_a[attribute][0]) == dict:
                    print(f'nested attr {attribute}')
                else:
                    print(f'list attr {attribute}')


if __name__ == '__main__':
    inst_a = {
        "id": "jvFnvkvv81SjJgqtv6arBA_0000",
        "full_name": "malcolm jones",
        "gender": "male",
        "birth_year": 1968,
        "birth_date": "1968-11-29",
        "industry": "internet",
        "job_title": "senior devops engineer",
        "job_title_role": "engineering",
        "job_title_sub_role": "devops",
        "job_title_levels": [
            "senior"
        ],
        "interests": [
            "getting back in touch",
            "lotus notes",
            "web applications",
            "web development",
            "reference requests",
            "web 2",
            "expertise requests",
            "new ventures",
            "data security",
            "programming",
            "java",
            "entrepreneurship",
            "network security",
            "social networking",
            "see 8",
            "php",
            "software engineering",
            "business deals",
            "mobile technologies",
            "new technology",
            "see less",
            "see 13",
            "mysql",
            "open source technologies"
        ],
        "skills": [
            "web development",
            "php",
            "mysql",
            "javascript",
            "jquery",
            "programming",
            "web applications",
            "linux",
            "html",
            "java",
            "cms",
            "sql",
            "devops",
            "networking",
            "social networking",
            "bash",
            "mongodb",
            "ubuntu",
            "node.js",
            "photoshop",
            "centos",
            "dns",
            "phing",
            "gearman",
            "puppet",
            "python",
            "system administration",
            "chef",
            "nagios",
            "rsync",
            "automation",
            "test automation",
            "ruby",
            "wireless networking",
            "git",
            "jenkins",
            "github",
            "build automation",
            "docker"
        ],
        "experience": [
            {
                "company": {
                    "name": "tidaltv.com",
                    "size": None,
                    "id": None,
                    "founded": None,
                    "industry": None,
                    "location": None,
                    "linkedin_url": None,
                    "linkedin_id": None,
                    "facebook_url": None,
                    "twitter_url": None,
                    "website": None
                },
                "location_names": [],
                "end_date": "2009-01-01",
                "start_date": "2008-08-01",
                "title": {
                    "name": "developer",
                    "role": "engineering",
                    "sub_role": None,
                    "levels": []
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "adobe",
                    "size": "10001+",
                    "id": "adobe",
                    "founded": 1982,
                    "industry": "computer software",
                    "location": {
                        "name": "san jose, california, united states",
                        "locality": "san jose",
                        "region": "california",
                        "metro": "san jose, california",
                        "country": "united states",
                        "continent": "north america",
                        "street_address": "345 park avenue",
                        "address_line_2": None,
                        "postal_code": "95110",
                        "geo": "37.33,-121.89"
                    },
                    "linkedin_url": "linkedin.com/company/adobe",
                    "linkedin_id": "1480",
                    "facebook_url": None,
                    "twitter_url": "twitter.com/adobe",
                    "website": "adobe.com"
                },
                "location_names": [
                    "new york, new york, united states"
                ],
                "end_date": None,
                "start_date": "2013-01",
                "title": {
                    "name": "senior devops engineer",
                    "role": "engineering",
                    "sub_role": "devops",
                    "levels": [
                        "senior"
                    ]
                },
                "is_primary": True
            },
            {
                "company": {
                    "name": "m-cubed information systems, inc.",
                    "size": "51-200",
                    "id": "m-cubed-information-systems-inc-",
                    "founded": 1985,
                    "industry": "information technology and services",
                    "location": {
                        "name": "silver spring, maryland, united states",
                        "locality": "silver spring",
                        "region": "maryland",
                        "metro": "district of columbia",
                        "country": "united states",
                        "continent": "north america",
                        "street_address": "8630 fenton street",
                        "address_line_2": "suite 925",
                        "postal_code": "20910",
                        "geo": "38.99,-77.02"
                    },
                    "linkedin_url": "linkedin.com/company/m-cubed-information-systems-inc-",
                    "linkedin_id": "3094308",
                    "facebook_url": None,
                    "twitter_url": "twitter.com/mcubedinfo",
                    "website": "mcubedinfo.com"
                },
                "location_names": [],
                "end_date": "2008-07",
                "start_date": "1998-06",
                "title": {
                    "name": "data security administrator and webmaster",
                    "role": None,
                    "sub_role": None,
                    "levels": []
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "behance",
                    "size": "51-200",
                    "id": "behance-inc-",
                    "founded": 2006,
                    "industry": "internet",
                    "location": {
                        "name": "new york, new york, united states",
                        "locality": "new york",
                        "region": "new york",
                        "metro": "new york, new york",
                        "country": "united states",
                        "continent": "north america",
                        "street_address": "532 broadway",
                        "address_line_2": None,
                        "postal_code": "10012",
                        "geo": "40.71,-74.00"
                    },
                    "linkedin_url": "linkedin.com/company/behance-inc-",
                    "linkedin_id": "151575",
                    "facebook_url": None,
                    "twitter_url": "twitter.com/behance",
                    "website": "behance.com"
                },
                "location_names": [
                    "new york, new york, united states"
                ],
                "end_date": "2016-11-13",
                "start_date": "2011-07-01",
                "title": {
                    "name": "web developer",
                    "role": "engineering",
                    "sub_role": "web",
                    "levels": []
                },
                "is_primary": False
            }
        ],
        "education": [
            {
                "school": {
                    "name": "morgan state university",
                    "type": "post-secondary institution",
                    "id": "14HZK6wL6MpMUnJsZ3jYPQ_0",
                    "location": {
                        "name": "baltimore, maryland, united states",
                        "locality": "baltimore",
                        "region": "maryland",
                        "country": "united states",
                        "continent": "north america"
                    },
                    "linkedin_url": "linkedin.com/school/morgan-state-university",
                    "facebook_url": "facebook.com/morganstateu",
                    "twitter_url": "twitter.com/morganstateu",
                    "linkedin_id": "18554",
                    "website": "morgan.edu",
                    "domain": "morgan.edu"
                },
                "degrees": [],
                "start_date": None,
                "end_date": "1991",
                "majors": [],
                "minors": [],
                "gpa": None
            },
            {
                "school": {
                    "name": "abraham clark high school",
                    "type": "secondary school",
                    "id": None,
                    "location": None,
                    "linkedin_url": None,
                    "facebook_url": None,
                    "twitter_url": None,
                    "linkedin_id": None,
                    "website": None,
                    "domain": None
                },
                "degrees": [],
                "start_date": None,
                "end_date": "1986",
                "majors": [],
                "minors": [],
                "gpa": None
            },
            {
                "school": {
                    "name": "university of virginia",
                    "type": "post-secondary institution",
                    "id": "-nZnOe5p6uHptwUwx7fL8w_0",
                    "location": {
                        "name": "charlottesville, virginia, united states",
                        "locality": "charlottesville",
                        "region": "virginia",
                        "country": "united states",
                        "continent": "north america"
                    },
                    "linkedin_url": "linkedin.com/school/university-of-virginia",
                    "facebook_url": "facebook.com/universityofvirginia",
                    "twitter_url": "twitter.com/uva",
                    "linkedin_id": "19604",
                    "website": "virginia.edu",
                    "domain": "virginia.edu"
                },
                "end_date": "2008",
                "start_date": "2004",
                "gpa": None,
                "degrees": [
                    "bachelors",
                    "bachelor of arts"
                ],
                "majors": [
                    "computer science"
                ],
                "minors": []
            }
        ]
    }
    inst_b = {
        "id": "xai9X--SNxN80tkF9o6sng_0000",
        "full_name": "willi gamboa",
        "gender": "male",
        "birth_year": None,
        "birth_date": None,
        "industry": "internet",
        "job_title": "senior software developer",
        "job_title_role": "engineering",
        "job_title_sub_role": "software",
        "job_title_levels": [
            "senior"
        ],
        "interests": [
            "education"
        ],
        "skills": [
            "javascript",
            "user experience",
            "css",
            "ajax",
            "web development",
            "node.js",
            "git",
            "jquery",
            "scrum",
            "html",
            "agile methodologies",
            "mysql",
            "selenium",
            "seo"
        ],
        "experience": [
            {
                "company": {
                    "name": "new york province of the society of jesus",
                    "size": None,
                    "id": None,
                    "founded": None,
                    "industry": None,
                    "location": None,
                    "linkedin_url": None,
                    "linkedin_id": None,
                    "facebook_url": None,
                    "twitter_url": None,
                    "website": None
                },
                "location_names": [],
                "end_date": "2005-04",
                "start_date": "2002-11",
                "title": {
                    "name": "it specialist and webmaster",
                    "role": "engineering",
                    "sub_role": "information_technology",
                    "levels": []
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "intuitive products international corporation",
                    "size": None,
                    "id": None,
                    "founded": None,
                    "industry": None,
                    "location": None,
                    "linkedin_url": None,
                    "linkedin_id": None,
                    "facebook_url": None,
                    "twitter_url": None,
                    "website": None
                },
                "location_names": [],
                "end_date": "2001-09",
                "start_date": "2000-03",
                "title": {
                    "name": "application developer",
                    "role": "engineering",
                    "sub_role": None,
                    "levels": []
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "time magazine",
                    "size": "501-1000",
                    "id": "time-magazine",
                    "founded": None,
                    "industry": "publishing",
                    "location": {
                        "name": "united states",
                        "locality": None,
                        "region": None,
                        "metro": None,
                        "country": "united states",
                        "continent": "north america",
                        "street_address": None,
                        "address_line_2": None,
                        "postal_code": None,
                        "geo": None
                    },
                    "linkedin_url": "linkedin.com/company/time-magazine",
                    "linkedin_id": "1748",
                    "facebook_url": "facebook.com/time",
                    "twitter_url": None,
                    "website": None
                },
                "location_names": [],
                "end_date": "2011-01",
                "start_date": "2006-06",
                "title": {
                    "name": "senior front end web developer",
                    "role": "engineering",
                    "sub_role": "web",
                    "levels": [
                        "senior"
                    ]
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "demdex, inc",
                    "size": "1-10",
                    "id": "demdex-inc",
                    "founded": None,
                    "industry": None,
                    "location": None,
                    "linkedin_url": "linkedin.com/company/demdex-inc",
                    "linkedin_id": None,
                    "facebook_url": None,
                    "twitter_url": None,
                    "website": None
                },
                "location_names": [],
                "end_date": "2011-02",
                "start_date": "2011-01",
                "title": {
                    "name": "front end engineer",
                    "role": "engineering",
                    "sub_role": "web",
                    "levels": []
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "td",
                    "size": "10001+",
                    "id": "td",
                    "founded": 2007,
                    "industry": "banking",
                    "location": {
                        "name": "toronto, ontario, canada",
                        "locality": "toronto",
                        "region": "ontario",
                        "metro": None,
                        "country": "canada",
                        "continent": "north america",
                        "street_address": None,
                        "address_line_2": None,
                        "postal_code": "m5k 1a2",
                        "geo": "43.70,-79.41"
                    },
                    "linkedin_url": "linkedin.com/company/td",
                    "linkedin_id": "2775",
                    "facebook_url": None,
                    "twitter_url": "twitter.com/td_canada",
                    "website": "td.com"
                },
                "location_names": [],
                "end_date": "2005-09",
                "start_date": "2005-04",
                "title": {
                    "name": "web development consultant",
                    "role": "engineering",
                    "sub_role": "web",
                    "levels": []
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "adp",
                    "size": "10001+",
                    "id": "adp",
                    "founded": 1949,
                    "industry": "human resources",
                    "location": {
                        "name": "roseland, new jersey, united states",
                        "locality": "roseland",
                        "region": "new jersey",
                        "metro": "new york, new york",
                        "country": "united states",
                        "continent": "north america",
                        "street_address": "1 adp boulevard",
                        "address_line_2": None,
                        "postal_code": "07068",
                        "geo": "40.82,-74.29"
                    },
                    "linkedin_url": "linkedin.com/company/adp",
                    "linkedin_id": "1463",
                    "facebook_url": "facebook.com/automaticdataprocessing",
                    "twitter_url": None,
                    "website": "adp.com"
                },
                "location_names": [],
                "end_date": "2000-03",
                "start_date": "1998-06",
                "title": {
                    "name": "data processing analyst",
                    "role": None,
                    "sub_role": None,
                    "levels": []
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "standard & poor's",
                    "size": "10001+",
                    "id": "spglobalratings",
                    "founded": None,
                    "industry": "capital markets",
                    "location": {
                        "name": "new york, new york, united states",
                        "locality": "new york",
                        "region": "new york",
                        "metro": "new york, new york",
                        "country": "united states",
                        "continent": "north america",
                        "street_address": "55 water street",
                        "address_line_2": None,
                        "postal_code": "10041",
                        "geo": "40.71,-74.00"
                    },
                    "linkedin_url": "linkedin.com/company/spglobalratings",
                    "linkedin_id": "3062",
                    "facebook_url": None,
                    "twitter_url": None,
                    "website": "standardandpoors.com"
                },
                "location_names": [],
                "end_date": "2006-05",
                "start_date": "2005-09",
                "title": {
                    "name": "front end web development consultant",
                    "role": "engineering",
                    "sub_role": "web",
                    "levels": []
                },
                "is_primary": False
            },
            {
                "company": {
                    "name": "adobe",
                    "size": "10001+",
                    "id": "adobe",
                    "founded": 1982,
                    "industry": "computer software",
                    "location": {
                        "name": "san jose, california, united states",
                        "locality": "san jose",
                        "region": "california",
                        "metro": "san jose, california",
                        "country": "united states",
                        "continent": "north america",
                        "street_address": "345 park avenue",
                        "address_line_2": None,
                        "postal_code": "95110",
                        "geo": "37.33,-121.89"
                    },
                    "linkedin_url": "linkedin.com/company/adobe",
                    "linkedin_id": "1480",
                    "facebook_url": None,
                    "twitter_url": "twitter.com/adobe",
                    "website": "adobe.com"
                },
                "location_names": [
                    "new york, new york, united states"
                ],
                "end_date": None,
                "start_date": "2011-02",
                "title": {
                    "name": "senior software developer",
                    "role": "engineering",
                    "sub_role": "software",
                    "levels": [
                        "senior"
                    ]
                },
                "is_primary": True
            }
        ],
        "education": [
            {
                "school": {
                    "name": "cornell university",
                    "type": "post-secondary institution",
                    "id": "4pGVlL6TZtjQib7zhfksEQ_0",
                    "location": {
                        "name": "ithaca, new york, united states",
                        "locality": "ithaca",
                        "region": "new york",
                        "country": "united states",
                        "continent": "north america"
                    },
                    "linkedin_url": "linkedin.com/school/cornell-university",
                    "facebook_url": "facebook.com/cornell",
                    "twitter_url": "twitter.com/cornell",
                    "linkedin_id": "18946",
                    "website": "cornell.edu",
                    "domain": "cornell.edu"
                },
                "end_date": "1998",
                "start_date": "1992",
                "gpa": None,
                "degrees": [
                    "bachelors",
                    "bachelor of science"
                ],
                "majors": [
                    "industrial engineering"
                ],
                "minors": []
            }
        ]
    }
    Distance(inst_a, inst_b).calc_distance()
