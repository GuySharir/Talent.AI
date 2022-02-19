"""
{companyA: [{name:val, age:val, skills:val, email:val}, {name:val, age:val, skills:val, email:val}, ...],
companyB: [{name:val, age:val, skills:val, email:val}, {name:val, age:val, skills:val, email:val}, ...],
...
"""
import json


class CleanData:
    def __init__(self, files: list, fields: list):
        self.files = files
        self.fields_list = fields
        self.data_per_company = {}

    def read_json_file(self, file_path, company_name):
        """
        Read relevant fields from company's json files
        """
        with open(file_path) as json_file:
            data = json.load(json_file)
            self.data_per_company[company_name] = []
            print("company - ", company_name)
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
            # print("after cleaning - ", self.data_per_company, "\n")

    def company_files(self):
        """
        Iterate throw all company's jsons
        """
        for file_path in self.files:
            company_name = file_path.split("\\")[1]
            print("########################################################")
            print("company - ", company_name)
            print("########################################################")
            self.read_json_file(file_path, company_name)

        # print("after cleaning - ", self.data_per_company, "\n")


if __name__ == '__main__':
    files_path = ["data\\AdobeEmployees.json", "data\\AmazonEmployees.json", "data\\AppleEmployees.json",
                  "data\\FacebookEmployees.json", "data\\GoogleEmployees.json", "data\\IbmEmployees.json",
                  "data\\MicrosoftEmployees.json", "data\\NvidiaEmployees.json", "data\\OracleEmployees.json",
                  "data\\SalesforceEmployees.json", "data\\TeslaEmployees.json", "data\\TwitterEmployees.json",
                  "data\\UberEmployees.json"]
    fields_list = ["id", "full_name", "gender", "birth_year", "birth_date", "industry", "job_title", "job_title_role",
                   "job_title_sub_role", "job_title_levels", "interests", "skills", "experience", "education"]
    CleanData(files_path, fields_list).company_files()
