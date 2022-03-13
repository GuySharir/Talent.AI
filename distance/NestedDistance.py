from distance.DistEnum import NestedDistMethod


class NestedDistance:
    def __init__(self, freq_per_attribute: dict, attribute: list, nested_obj1: dict, nested_obj2):
        self.freq_per_attribute = freq_per_attribute
        self.attribute = attribute
        self.nested_obj1 = nested_obj1
        self.nested_obj2 = nested_obj2

    def calc_dist(self):
        if self.attribute == 'education':
            self.education_dist()
        elif self.attribute == 'experience':
            self.experience_dist()

    def education_dist(self):
        print(f"degrees values {self.freq_per_attribute['degrees']}")
        print(f"majors values {self.freq_per_attribute['majors']}")
        print(f"unique values from major {set(self.freq_per_attribute['majors'])}")
        degree_levels = ['bachelors', 'masters', 'doctorates', 'associates']
        major = ['computer science', 'software engineering', 'engineering', 'philosophy', 'electronics', 'marketing',
                 'music', 'business', 'electrical engineering', 'information systems', 'general education',
                 'visual communications', 'art', 'data science', 'dental hygiene', 'computer engineering', 'economics',
                 'finance', 'information science', 'geography', 'project management', 'communications',
                 'film', 'literature', 'english language', 'organizational leadership', 'ministry']
        print(f'attr {self.attribute}')
        print(f'obj1 {self.nested_obj1}')
        print(f'obj2 {self.nested_obj2}')

    def experience_dist(self):
        pass
