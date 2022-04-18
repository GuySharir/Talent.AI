from ReadData import read_freq_per_value_data, read_domain_per_attr_data, DATA_TYPE_PER_INDEX, ATTRIBUTE_PER_INDEX, DATA_TYPE_PER_INDEX_EXPERIENCE, DATA_TYPE_PER_INDEX_EDUCATION, EXPERIENCE_OBJECT_ATTR_LENGTH, EDUCATION_OBJECT_ATTR_LENGTH
from dataTool.runtimeObjectsInfo.ListLengthData import LIST_LENGTH_PER_ATTR, NESTED_LENGTH_PER_ATTR, EXPERIENCE_LISTS_LENGTH, EDUCATION_LISTS_LENGTH
from DistEnum import DistMethod
from DistFunctions import DistanceData, q14, categorical_dist_between_freq_vectors, numerical_dist_between_freq_vectors


def logger(*args):
    print(*args)


class DistanceFlow:
    def __init__(self, vec1: list, vec2: list, representation_option: DistMethod, representation_option_set: DistMethod):
        self.vec1 = vec1
        self.vec2 = vec2
        self.inx = 0

        self.representation_option = representation_option
        self.representation_option_set = representation_option_set

        self.cat_distance_result = []
        self.num_distance_result = []
        self.freq_distance_result = None
        self.total_distance_result = None

    def numerical_distance(self, representation_option: DistMethod, attr_type, num1, num2):

        if representation_option == DistMethod.fix_length_freq:
            self.num_distance_result.append(numerical_dist_between_freq_vectors(attr_type=attr_type,
                                                                                num_val1=num1, num_val2=num2))

    def categorical_distance(self, representation_option: DistMethod, attr_type, frequency: dict, domain_size: int):

        if representation_option == DistMethod.fix_length_freq:
            data = DistanceData(instance1=self.vec1, instance2=self.vec2, val1_frequency=self.vec1[self.inx],
                                val2_frequency=self.vec2[self.inx], frequency=frequency,
                                domain_size=domain_size, attribute_inx=self.inx)
            self.cat_distance_result.append(categorical_dist_between_freq_vectors(attr_type=attr_type, data=data))

    def set_distance(self, attr_name: str, frequency: dict, domain_size: int):
        # each set contains only categorical values in different representations
        attr_length = LIST_LENGTH_PER_ATTR[attr_name]
        set1 = self.vec1[self.inx: self.inx + attr_length]
        set2 = self.vec2[self.inx: self.inx + attr_length]

        logger(f'set1-\n{set1}')
        logger(f'set2-\n{set2}')

        if self.representation_option_set == DistMethod.fix_length_freq:
            for _ in range(attr_length):
                self.categorical_distance(representation_option=self.representation_option_set, attr_type=str, frequency=frequency, domain_size=domain_size)
                self.inx += 1

        self.inx = self.inx - 1

    def nested_distance(self, attr_name: str, frequency: dict, domain_size: int):
        if attr_name == 'experience':
            attr_length = (sum(EXPERIENCE_LISTS_LENGTH.values()) + EXPERIENCE_OBJECT_ATTR_LENGTH - len(
                EXPERIENCE_LISTS_LENGTH.keys())) * NESTED_LENGTH_PER_ATTR[attr_name]
        elif attr_name == 'education':
            attr_length = (sum(EDUCATION_LISTS_LENGTH.values()) + EDUCATION_OBJECT_ATTR_LENGTH - len(
                EDUCATION_LISTS_LENGTH.keys())) * NESTED_LENGTH_PER_ATTR[attr_name]
        print()

    def calc_distance(self):
        domain = read_domain_per_attr_data()
        freq = read_freq_per_value_data()

        for raw_data_inx, data_type in DATA_TYPE_PER_INDEX.items():
            attr = ATTRIBUTE_PER_INDEX[raw_data_inx]
            attr_freq = freq[attr]
            attr_domain = domain[attr]

            if data_type == str:
                self.categorical_distance(representation_option=self.representation_option, attr_type=data_type, frequency=attr_freq, domain_size=attr_domain)

            elif data_type == float or data_type == int:
                self.numerical_distance(representation_option=self.representation_option, attr_type=data_type, num1=self.vec1[self.inx],
                                        num2=self.vec2[self.inx])

            elif data_type == list:
                self.set_distance(attr_name=attr, frequency=attr_freq, domain_size=attr_domain)

            elif data_type == dict:
                self.nested_distance(attr_name=attr, frequency=attr_freq, domain_size=attr_domain)

            self.inx += 1

        print(f'categorical result-\n {self.cat_distance_result}')
        print(f'categorical list length-\n {len(self.cat_distance_result)}')
        print(f'numerical result-\n {self.num_distance_result}')
        self.freq_distance_result = q14(categorical_sum=sum(self.cat_distance_result), numerical_sum=sum(self.num_distance_result))
        print(f'distance result-\n {self.freq_distance_result}')


def run_distance(vec1: list, vec2: list, representation_option: DistMethod, representation_option_set: DistMethod):
    DistanceFlow(vec1=vec1, vec2=vec2, representation_option=representation_option, representation_option_set=representation_option_set).calc_distance()


if __name__ == '__main__':
    instance1_ = {'laura gao': ('twitter', [1, 1, 1, 5, 1996.0, 57, 14, 1, 7, 7, 1, 61, 61, 4, 1, 1, 1, 1, 14, 10, 7, 1, 1])}
    instance2_ = {'bruk argaw': ('twitter', [1, 1, 1, 93, 1991.0, 1, 14, 18, 88, 82, 1, 61, 61, 1, 34, 28, 22, 10, 14, 11, 10, 6, 1])}

    vec1_ = [1, 1, 1, 5, 1996.0, 57, 14, 1, 7, 7, 1, 61, 61, 4, 1, 1, 1, 1, 14, 10, 7, 1, 1]
    vec2_ = [1, 1, 1, 93, 1991.0, 1, 14, 18, 88, 82, 1, 61, 61, 1, 34, 28, 22, 10, 14, 11, 10, 6, 1]
    run_distance(vec1=vec1_, vec2=vec2_, representation_option=DistMethod.fix_length_freq, representation_option_set=DistMethod.fix_length_freq)
