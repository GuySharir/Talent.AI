"""
{companyA: [{name:val, age:val, skills:val, email:val}, {name:val, age:val, skills:val, email:val}, ...],
companyB: [{name:val, age:val, skills:val, email:val}, {name:val, age:val, skills:val, email:val}, ...],
...
"""
import json


class CleanData:
    def __init__(self, file: str, fields: list, company: str):
        self.file_name = file
        self.company_name = company
        self.fields_list = fields
        self.data_per_company = {}

    def read_json_file(self):
        with open(self.file_name) as json_file:
            data = json.load(json_file)
            self.data_per_company[self.company_name] = []
            for p in data:
                print("p- ", p, "\n")
                self.data_per_company[self.company_name].append({
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
            print("after cleaning - ", self.data_per_company, "\n")


if __name__ == '__main__':
    fields_list = ["id", "full_name", "gender", "birth_year", "birth_date", "industry", "job_title", "job_title_role",
                   "job_title_sub_role", "job_title_levels", "interests", "skills", "experience", "education"]
    CleanData("data\\AdobeEmployees.json", fields_list, "Adobe").read_json_file()

