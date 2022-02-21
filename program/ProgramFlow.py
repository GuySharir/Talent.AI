from algorithems.NumDistance import NumDistance
from program.cleanData import CleanData
import json


class Program:
    """
        This class (Program) is responsible for the clean data and distance calculation flow
        - self.files, list of json files contains employees data
        - self.fields_list, list of relevant attributes to extract from employees' data
        - data_per_company, a dictionary contains employees data per company
        - numeric_attr_dist, a dictionary contains the attribute name and the distance result for numerical data
        - categorical_attr_dist, a dictionary contains the attribute name and the distance result for categorical data

        """
    def __init__(self, files: list, fields: list, clean_data_path):
        self.files = files
        self.fields_list = fields
        self.clean_data_path = clean_data_path
        self.data_per_company = {}
        self.numeric_attr_dist = {}
        self.categorical_attr_dist = {}

    def get_employee_data(self):
        self.data_per_company = CleanData(files_path, fields_list).company_files()
        for company in self.data_per_company.keys():
            print("Company After cleaning - ", company, "\n")
            print("employees per company after cleaning - ", self.data_per_company[company], "\n")
            file_name = self.clean_data_path + '\\' + company + '.json'

            with open(file_name, 'w') as fp:
                json.dump(self.data_per_company[company], fp, indent=4)
            # for data in self.data_per_company[company]:
            #     print("item After cleaning - ", data)

    def calc_distance(self):
        pass


if __name__ == '__main__':
    files_path = ["C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
                  "\\data\\AdobeEmployees.json"]
    # files_path = ["C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\AdobeEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\AmazonEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\AppleEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\FacebookEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\GoogleEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\IbmEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\MicrosoftEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\NvidiaEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\OracleEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\SalesforceEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\TeslaEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\TwitterEmployees.json",
    #               "C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
    #               "\\data\\UberEmployees.json"]
    fields_list = ["id", "full_name", "gender", "birth_year", "birth_date", "industry", "job_title", "job_title_role",
                   "job_title_sub_role", "job_title_levels", "interests", "skills", "experience", "education"]
    clean_data = 'C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool' \
                 '\\clean_data'
    Program(files_path, fields_list, clean_data).get_employee_data()
