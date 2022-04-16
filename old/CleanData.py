import json
import os


class Education:
    """
    """

    def __init__(self, education: dict):

        self.school_name = None
        self.school_type = None
        if education["school"]:
            self.school_name = education["school"]["name"]
            self.school_type = education["school"]["type"]

        self.end_date = education["end_date"]
        self.start_date = education["start_date"]
        self.gpa = education["gpa"]
        self.degrees = education["degrees"]
        self.majors = education["majors"]
        self.minors = education["minors"]


class Experience:
    def __init__(self, experience: dict):
        self.company_name = experience['company']["name"]
        self.company_size = experience['company']["size"]
        self.company_id = experience['company']["id"]
        self.company_founded = experience['company']["founded"]
        self.company_industry = experience['company']["industry"]
        self.end_date = experience["end_date"]
        self.start_date = experience["start_date"]
        self.current_job = experience["is_primary"]

        self.company_location_name = None
        self.company_location_country = None
        self.company_location_continent = None

        self.title_name = None
        self.title_role = None
        self.title_levels = None

        if experience["company"]["location"]:
            self.company_location_name = experience["company"]["location"]["name"]
            self.company_location_country = experience["company"]["location"]["country"]
            self.company_location_continent = experience["company"]["location"]["continent"]

        if experience["title"]:
            self.title_name = experience["title"]["name"]
            self.title_role = experience["title"]["role"]
            self.title_levels = experience["title"]["levels"]


class Employee:
    def __init__(self, entry) -> None:
        # print(entry)
        self.full_name = entry["full_name"]
        self.first_name = entry["first_name"]
        self.last_name = entry["last_name"]
        self.gender = entry["gender"]
        self.birth_year = entry["birth_year"]
        self.birth_date = entry["birth_date"]
        self.industry = entry["industry"]
        self.job_title = entry["job_title"]
        self.job_title_role = entry["job_title_role"]
        self.job_title_sub_role = entry["job_title_sub_role"]
        self.job_title_levels = entry["job_title_levels"]
        self.job_company_id = entry["job_company_id"]
        self.job_company_name = entry["job_company_name"]
        self.job_start_date = entry["job_start_date"]
        self.interests = entry["interests"]
        self.skills = entry["skills"]

        self.experience = []
        self.education = []
        self.generate_experience_list(entry["experience"])
        self.generate_education_list(entry["education"])

    def generate_experience_list(self, experience) -> list:
        for exp in experience:
            self.experience.append(vars(Experience(exp)))

    def generate_education_list(self, education) -> list:
        for edu in education:
            self.education.append(vars(Education(edu)))


class CleanData:
    """
    This class (CleanData) accepts paths to all json data and extract relevant attributes
    paths: a list of paths to raw data files
    - self.json_data, temporary iterable for each json data file
    - self.clean_data, cleaned extracted data dictionary, each company name is the key and the value is the data

    """

    def __init__(self, paths: list):
        self.paths: list = paths
        self.json_data: list = []
        self.cleaned_data: dict = dict()
        self.clean()

    def read_json_file(self, file_path: str):
        with open(file_path) as json_file:
            self.json_data = json.load(json_file)

    def clean(self):
        """
            iterate through the provided paths and for each path clean the data
        """

        for path in self.paths:
            company_name = (path.split("/")[-1]).replace(".json", "")
            print(company_name)
            self.read_json_file(path)
            self.cleaned_data[company_name] = []

            for employee in self.json_data:
                # print(employee)
                self.cleaned_data[company_name].append(
                    vars(Employee(employee)))

    def save(self, path: str):
        """
            save the cleaned data to location 'path' property
            'path' : a path to where the file should be saved.
            final result - cleaned data will be saved to files at /<path>/<company_name>Employees.json
        """
        for key in self.cleaned_data.keys():
            file_name = f"{path}/{key}.json"
            with open(file_name, 'w') as dest:
                json.dump(self.cleaned_data[key], dest, indent=4)


if __name__ == '__main__':

    PROJECT_ROOT = "/Users/guyshenkar/Documents/private/final project/Talent.AI/"
    paths = []

    for path in os.listdir(f"{PROJECT_ROOT}/dataTool/data"):
        paths.append(os.path.join(f"{PROJECT_ROOT}/dataTool/data", path))

    x = CleanData(paths)
    x.save(f"{PROJECT_ROOT}/dataTool/clean_data")
