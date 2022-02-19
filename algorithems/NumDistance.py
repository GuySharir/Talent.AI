class NumDistance:
    """
    This class (NumDistance) calculate distance between two values
    of a single numerical attribute
    - self.numeric_attr_dist, is the return value. A dictionary contains the attribute name and
    the distance result
    {age: val, birth_year: val}
    - instance_a, instance_b, dictionary contains employee data
    {'name': 'Andrew', 'birth_year': 1968, 'birth_date': '1968-11-29'}
    """
    def __init__(self, instance_a: dict, instance_b: dict):
        self.numeric_attr_dist = {}
        self.instance_a = instance_a
        self.instance_b = instance_b

    def calc_num_distance(self, attribute: str) -> float:
        return (self.instance_a[attribute] - self.instance_b[attribute]) ** 2

    def find_numeric_attr(self) -> dict:
        for attribute in self.instance_a.keys():
            print(f'attribute {attribute} is int? {isinstance(self.instance_a.get(attribute), int)}')
            if isinstance(self.instance_a.get(attribute), int) or isinstance(self.instance_a.get(attribute), float):
                self.numeric_attr_dist[attribute] = self.calc_num_distance(attribute)
        print("numeric_attr_dist- ", self.numeric_attr_dist)
        return self.numeric_attr_dist


if __name__ == '__main__':
    inst_a = {'id': 'jvFnvkvv81SjJgqtv6arBA_0000', 'full_name': 'malcolm jones', 'gender': 'male',
                    'birth_year': 1968, 'birth_date': '1968-11-29', 'industry': 'internet',
                    'job_title': 'senior devops engineer'}
    inst_b = {'id': '4zFdHP9y7euI9bwujI3Wmw_0000', 'full_name': 'kyle warneck', 'gender': 'male',
                    'birth_year': 1983, 'birth_date': None, 'industry': 'internet',
                    'job_title': 'senior software engineer, ad cloud developer productivity team'}
    NumDistance(inst_a, inst_b).find_numeric_attr()
