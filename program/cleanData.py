import json


class CleanData:
    """
    This class (CleanData) takes all json data and extract relevant attributes
    - the return value (self.data_per_company) is a dictionary as shown below
    {companyA: [{name:val, age:val, skills:val, email:val, ...}, {name:val, age:val, skills:val, email:val, ...}, ...],
    companyB: [{name:val, age:val, skills:val, email:val, ...}, {name:val, age:val, skills:val, email:val, ...}, ...],
    ...}
    - self.files, list of json files contains employees data
    - self.fields_list, list of relevant attributes to extract from employees' data

    """
    def __init__(self, files: list, fields: list):
        self.files = files
        self.fields_list = fields
        self.data_per_company = {}

    def read_json_file(self, file_path, company_name):
        with open(file_path) as json_file:
            data = json.load(json_file)
            self.data_per_company[company_name] = []
            # print("company - ", company_name)
            for p in data:
                # print("p- ", p, "\n")
                self.data_per_company[company_name].append({
                    self.fields_list[0]: p[self.fields_list[0]],
                    self.fields_list[1]: p[self.fields_list[1]],
                    self.fields_list[2]: p[self.fields_list[2]],
                    self.fields_list[3]: p[self.fields_list[3]],
                    self.fields_list[4]: p[self.fields_list[4]],
                    self.fields_list[5]: p[self.fields_list[5]],
                    self.fields_list[6]: p[self.fields_list[6]],
                    self.fields_list[7]: p[self.fields_list[7]],
                    self.fields_list[8]: p[self.fields_list[8]],
                    self.fields_list[9]: p[self.fields_list[9]],
                    self.fields_list[10]: p[self.fields_list[10]],
                    self.fields_list[11]: p[self.fields_list[11]],
                    self.fields_list[12]: p[self.fields_list[12]],
                    self.fields_list[13]: p[self.fields_list[13]]
                })

    def company_files(self) -> dict:
        for file_path in self.files:
            company_name = (file_path.split("\\")[-1]).replace(".json", "")
            self.read_json_file(file_path, company_name)

        return self.data_per_company


if __name__ == '__main__':
    # files_path = ["data\\AdobeEmployees.json", "data\\AmazonEmployees.json", "data\\AppleEmployees.json",
    #               "data\\FacebookEmployees.json", "data\\GoogleEmployees.json", "data\\IbmEmployees.json",
    #               "data\\MicrosoftEmployees.json", "data\\NvidiaEmployees.json", "data\\OracleEmployees.json",
    #               "data\\SalesforceEmployees.json", "data\\TeslaEmployees.json", "data\\TwitterEmployees.json",
    #               "data\\UberEmployees.json"]
    files_path = ["C:\\Users\\opalp\\Documents\\opalpeltzman\\4thYearSemesterA\\final project\\Talent.AI\\dataTool"
                  "\\data\\AdobeEmployees.json"]
    fields_list = ["id", "full_name", "gender", "birth_year", "birth_date", "industry", "job_title", "job_title_role",
                   "job_title_sub_role", "job_title_levels", "interests", "skills", "experience", "education"]
    CleanData(files_path, fields_list).company_files()
