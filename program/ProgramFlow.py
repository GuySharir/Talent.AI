from algorithems.NumDistance import NumDistance
from program.cleanData import CleanData


class Program:
    """
        This class (Program) is responsible for the clean data and distance calculation flow
        - self.files, list of json files contains employees data
        - self.fields_list, list of relevant attributes to extract from employees' data
        - data_per_company, a dictionary contains employees data per company
        - numeric_attr_dist, a dictionary contains the attribute name and the distance result for numerical data
        - categorical_attr_dist, a dictionary contains the attribute name and the distance result for categorical data

        """
    def __init__(self, files: list, fields: list):
        self.files = files
        self.fields_list = fields
        self.data_per_company = {}
        self.numeric_attr_dist = {}
        self.categorical_attr_dist = {}
        self.get_employee_data()

    def get_employee_data(self):
        self.data_per_company = CleanData(files_path, fields_list).company_files()
        for company in self.data_per_company.keys():
            print("Company After cleaning - ", company, "\n")
            for data in self.data_per_company[company]:
                print("item After cleaning - ", data)

    def calc_distance(self):
        pass


if __name__ == '__main__':
    files_path = ["C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
                  "\\data\\AdobeEmployees.json"]
    fields_list = ["id", "full_name", "gender", "birth_year", "birth_date", "industry", "job_title", "job_title_role",
                   "job_title_sub_role", "job_title_levels", "interests", "skills", "experience", "education"]

    Program(files_path, fields_list)