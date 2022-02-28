from algorithems.NumDistance import NumDistance
from program.cleanData import CleanData
import json


class Distance:
    """
        This class (Program) is responsible for the distance calculation

        contains q11, q12, q14 categorical distance calculation equations based on
        "An incremental mixed data clustering method using a new distance measure"
        article. (published on 6 may 2014)

        - self.files, list of json files contains employees data
        - self.fields_list, list of relevant attributes to extract from employees' data
        - clean_data_path, path to a folder where we save all cleaned data
        - data_per_company, a dictionary contains employees data per company
        - attr_type, a dictionary contains the attribute name and the distance result for numerical data


    """
    def __init__(self, instance_a: object, instance_b: object, attr_type: dict):
        self.attr_type = attr_type
        self.attr_dist_result = {}
        self.instance_a = instance_a
        self.instance_b = instance_b

    def q12(self, attribute):
        if self.instance_a[attribute] == self.instance_b[attribute]:
            return 0
        elif self.instance_a[attribute] != self.instance_b[attribute]:
            return 1

    def q11(self):
        pass

    def q14(self):
        pass

    def calc_distance(self):
        # self.attr_type = {attribute: type(self.instance_a.get(attribute)) for attribute in self.instance_a.keys()}
        # # print(self.attr_type)
        # for inx, attr in enumerate(self.attr_type.keys()):
            # print(f'attribute - {attr} \n value - {self.instance_a[inx]}')

        self.instance_a = {attr: self.instance_a[inx] for inx, attr in enumerate(self.attr_type.keys())}
        self.instance_b = {attr: self.instance_b[inx] for inx, attr in enumerate(self.attr_type.keys())}
        print(f'instance a - {self.instance_a}')
        print(f'instance b - {self.instance_b}')


if __name__ == '__main__':
    inst_a = {
        "full_name": "malcolm jones",
        "first_name": "malcolm",
        "last_name": "jones",
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
        "job_company_id": "adobe",
        "job_company_name": "adobe",
        "job_start_date": "2013-01",
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
                "company_name": "tidaltv.com",
                "company_size": None,
                "company_id": None,
                "company_founded": None,
                "company_industry": None,
                "end_date": "2009-01-01",
                "start_date": "2008-08-01",
                "current_job": False,
                "company_location_name": None,
                "company_location_country": None,
                "company_location_continent": None,
                "title_name": "developer",
                "title_role": "engineering",
                "title_levels": []
            },
            {
                "company_name": "adobe",
                "company_size": "10001+",
                "company_id": "adobe",
                "company_founded": 1982,
                "company_industry": "computer software",
                "end_date": None,
                "start_date": "2013-01",
                "current_job": True,
                "company_location_name": "san jose, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "senior devops engineer",
                "title_role": "engineering",
                "title_levels": [
                    "senior"
                ]
            },
            {
                "company_name": "m-cubed information systems, inc.",
                "company_size": "51-200",
                "company_id": "m-cubed-information-systems-inc-",
                "company_founded": 1985,
                "company_industry": "information technology and services",
                "end_date": "2008-07",
                "start_date": "1998-06",
                "current_job": False,
                "company_location_name": "silver spring, maryland, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "data security administrator and webmaster",
                "title_role": None,
                "title_levels": []
            },
            {
                "company_name": "behance",
                "company_size": "51-200",
                "company_id": "behance-inc-",
                "company_founded": 2006,
                "company_industry": "internet",
                "end_date": "2016-11-13",
                "start_date": "2011-07-01",
                "current_job": False,
                "company_location_name": "new york, new york, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "web developer",
                "title_role": "engineering",
                "title_levels": []
            }
        ],
        "education": [
            {
                "school_name": "morgan state university",
                "school_type": "post-secondary institution",
                "end_date": "1991",
                "start_date": None,
                "gpa": None,
                "degrees": [],
                "majors": [],
                "minors": []
            },
            {
                "school_name": "abraham clark high school",
                "school_type": "secondary school",
                "end_date": "1986",
                "start_date": None,
                "gpa": None,
                "degrees": [],
                "majors": [],
                "minors": []
            },
            {
                "school_name": "university of virginia",
                "school_type": "post-secondary institution",
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
        "full_name": "kyle warneck",
        "first_name": "kyle",
        "last_name": "warneck",
        "gender": "male",
        "birth_year": 1983,
        "birth_date": None,
        "industry": "internet",
        "job_title": "senior software engineer, ad cloud developer productivity team",
        "job_title_role": "engineering",
        "job_title_sub_role": "devops",
        "job_title_levels": [
            "senior"
        ],
        "job_company_id": "adobe",
        "job_company_name": "adobe",
        "job_start_date": "2020-06",
        "interests": [
            "saas",
            "social services",
            "community technology network",
            "politics",
            "education",
            "big data",
            "volunteer computer instructor",
            "pomona college",
            "analytics",
            "poverty alleviation",
            "science and technology",
            "bridging online and offline",
            "alumni admissions volunteer"
        ],
        "skills": [
            "product management",
            "market research",
            "public speaking",
            "data analysis",
            "analytics",
            "javascript",
            "css",
            "survey research",
            "project management",
            "leadership",
            "html",
            "survey design",
            "account management",
            "scrum",
            "jquery",
            "management",
            "user experience",
            "salesforce.com",
            "marketing strategy",
            "marketing research",
            "marketing",
            "node.js",
            "product development",
            "backbone.js",
            "mongodb",
            "surveys",
            "python",
            "coffeescript",
            "powerpoint",
            "microsoft excel",
            "excel",
            "computer instruction",
            "angularjs",
            "tdd"
        ],
        "experience": [
            {
                "company_name": "adobe",
                "company_size": "10001+",
                "company_id": "adobe",
                "company_founded": 1982,
                "company_industry": "computer software",
                "end_date": None,
                "start_date": "2020-06",
                "current_job": True,
                "company_location_name": "san jose, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "senior software engineer, ad cloud developer productivity team",
                "title_role": "engineering",
                "title_levels": [
                    "senior"
                ]
            },
            {
                "company_name": "product plus reclamebureau",
                "company_size": "11-50",
                "company_id": "product-plus-reclamebureau",
                "company_founded": 1984,
                "company_industry": "marketing and advertising",
                "end_date": "2007-04",
                "start_date": "2005-06",
                "current_job": False,
                "company_location_name": "netherlands",
                "company_location_country": "netherlands",
                "company_location_continent": "europe",
                "title_name": "account manager - purchasing and sales",
                "title_role": "finance",
                "title_levels": [
                    "manager"
                ]
            },
            {
                "company_name": "markettools",
                "company_size": "201-500",
                "company_id": "markettools-inc.",
                "company_founded": 1997,
                "company_industry": "market research",
                "end_date": "2010-05",
                "start_date": "2008-08",
                "current_job": False,
                "company_location_name": "san francisco, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "sample analyst, online surveys",
                "title_role": None,
                "title_levels": []
            },
            {
                "company_name": "surveymonkey",
                "company_size": "501-1000",
                "company_id": "surveymonkey",
                "company_founded": 1999,
                "company_industry": "internet",
                "end_date": "2013-06",
                "start_date": "2012-01",
                "current_job": False,
                "company_location_name": "san mateo, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "product manager, zoompanel",
                "title_role": "operations",
                "title_levels": [
                    "manager"
                ]
            },
            {
                "company_name": "john edwards for president",
                "company_size": "51-200",
                "company_id": "john-edwards-for-president",
                "company_founded": None,
                "company_industry": "political organization",
                "end_date": "2008-01",
                "start_date": "2007-05",
                "current_job": False,
                "company_location_name": "united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "field organizer - iowa caucus",
                "title_role": None,
                "title_levels": []
            },
            {
                "company_name": "markettools",
                "company_size": "201-500",
                "company_id": "markettools-inc.",
                "company_founded": 1997,
                "company_industry": "market research",
                "end_date": "2011-06",
                "start_date": "2010-05",
                "current_job": False,
                "company_location_name": "san francisco, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "account manager, sample sales",
                "title_role": "sales",
                "title_levels": [
                    "manager"
                ]
            },
            {
                "company_name": "markettools",
                "company_size": "201-500",
                "company_id": "markettools-inc.",
                "company_founded": 1997,
                "company_industry": "market research",
                "end_date": "2012-01",
                "start_date": "2011-07",
                "current_job": False,
                "company_location_name": "san francisco, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "assoc product manager and assoc panel manager - zoompanel",
                "title_role": "operations",
                "title_levels": [
                    "manager"
                ]
            },
            {
                "company_name": "adobe",
                "company_size": "10001+",
                "company_id": "adobe",
                "company_founded": 1982,
                "company_industry": "computer software",
                "end_date": "2020-06",
                "start_date": "2017-01",
                "current_job": False,
                "company_location_name": "san jose, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "lead frontend engineer, ad cloud tv",
                "title_role": "engineering",
                "title_levels": [
                    "manager"
                ]
            },
            {
                "company_name": "tubemogul, inc.",
                "company_size": "501-1000",
                "company_id": "tubemogul-inc-",
                "company_founded": 2006,
                "company_industry": "marketing and advertising",
                "end_date": "2017-01",
                "start_date": "2015-10",
                "current_job": False,
                "company_location_name": "emeryville, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "software engineer, web",
                "title_role": "engineering",
                "title_levels": []
            },
            {
                "company_name": "good eggs",
                "company_size": "201-500",
                "company_id": "good-eggs",
                "company_founded": 2011,
                "company_industry": "food production",
                "end_date": "2015-08",
                "start_date": "2014-04",
                "current_job": False,
                "company_location_name": "san francisco, california, united states",
                "company_location_country": "united states",
                "company_location_continent": "north america",
                "title_name": "software engineer",
                "title_role": "engineering",
                "title_levels": []
            }
        ],
        "education": [
            {
                "school_name": "pomona college",
                "school_type": "post-secondary institution",
                "end_date": "2014",
                "start_date": None,
                "gpa": None,
                "degrees": [],
                "majors": [],
                "minors": []
            },
            {
                "school_name": "bellarmine college preparatory",
                "school_type": "post-secondary institution",
                "end_date": "2001",
                "start_date": "1997",
                "gpa": None,
                "degrees": [],
                "majors": [],
                "minors": []
            },
            {
                "school_name": "pomona college",
                "school_type": "post-secondary institution",
                "end_date": "2005",
                "start_date": "2001",
                "gpa": None,
                "degrees": [
                    "bachelors",
                    "bachelor of arts"
                ],
                "majors": [
                    "sociology"
                ],
                "minors": []
            }
        ]
    }
    Distance(inst_a, inst_b).calc_distance()
