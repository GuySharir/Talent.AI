from program.ReadData import read_freq_per_value_data, read_domain_per_attr_data, DATA_TYPE_PER_INDEX, \
    ATTRIBUTE_PER_INDEX, DATA_TYPE_PER_INDEX_EXPERIENCE, DATA_TYPE_PER_INDEX_EDUCATION, EXPERIENCE_OBJECT_ATTR_LENGTH, \
    EDUCATION_OBJECT_ATTR_LENGTH, EXPERIENCE_ATTRIBUTE_PER_INDEX, EDUCATION_ATTRIBUTE_PER_INDEX
from dataTool.runtimeObjectsInfo.ListLengthData import LIST_LENGTH_PER_ATTR, NESTED_LENGTH_PER_ATTR, \
    EXPERIENCE_LISTS_LENGTH, EDUCATION_LISTS_LENGTH
from program.DistEnum import DistMethod
from program.DistFunctions import DistanceData, q14, categorical_dist_between_freq_vectors, \
    numerical_dist_between_freq_vectors


def logger(*args):
    # print(*args)
    pass


class DistanceFlow:
    def __init__(self, vec1: list, vec2: list, representation_option: DistMethod,
                 representation_option_set: DistMethod):
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
            result = categorical_dist_between_freq_vectors(attr_type=attr_type, data=data)
            logger(f'categorical result {result}')
            self.cat_distance_result.append(result)
            # self.cat_distance_result.append(categorical_dist_between_freq_vectors(attr_type=attr_type, data=data))

    def set_distance(self, attr_name: str, frequency: dict, domain_size: int):
        # each set contains only categorical values in different representations
        attr_length = LIST_LENGTH_PER_ATTR[attr_name]
        set1 = self.vec1[self.inx: self.inx + attr_length]
        set2 = self.vec2[self.inx: self.inx + attr_length]

        logger(f'set1-\n{set1}')
        logger(f'set2-\n{set2}')

        if self.representation_option_set == DistMethod.fix_length_freq:
            for _ in range(attr_length):
                self.categorical_distance(representation_option=self.representation_option_set, attr_type=str,
                                          frequency=frequency, domain_size=domain_size)
                self.inx += 1

        self.inx = self.inx - 1

    def nested_distance(self, attr_name: str, frequency: dict, domain_size: dict):
        num_of_nested_objects = NESTED_LENGTH_PER_ATTR[attr_name]
        if attr_name == 'experience':
            attr_data_type_per_index = DATA_TYPE_PER_INDEX_EXPERIENCE
            attr_per_index = EXPERIENCE_ATTRIBUTE_PER_INDEX
            # attr_length = (sum(EXPERIENCE_LISTS_LENGTH.values()) + EXPERIENCE_OBJECT_ATTR_LENGTH - len(
            #     EXPERIENCE_LISTS_LENGTH.keys())) * NESTED_LENGTH_PER_ATTR[attr_name]
        else:  # attr_name == 'education'
            attr_data_type_per_index = DATA_TYPE_PER_INDEX_EDUCATION
            attr_per_index = EDUCATION_ATTRIBUTE_PER_INDEX
            # attr_length = (sum(EDUCATION_LISTS_LENGTH.values()) + EDUCATION_OBJECT_ATTR_LENGTH - len(
            #     EDUCATION_LISTS_LENGTH.keys())) * NESTED_LENGTH_PER_ATTR[attr_name]
        for loop_inx in range(num_of_nested_objects):
            for raw_data_inx, data_type in attr_data_type_per_index.items():
                attr = attr_per_index[raw_data_inx]
                logger(f'attribute {attr} in for loop num {loop_inx}')
                if data_type == str or data_type == bool:
                    attr_freq = frequency[attr]
                    attr_domain = domain_size[attr]
                    self.categorical_distance(representation_option=self.representation_option, attr_type=data_type,
                                              frequency=attr_freq, domain_size=attr_domain)

                elif data_type == float or data_type == int:
                    self.numerical_distance(representation_option=self.representation_option, attr_type=data_type,
                                            num1=self.vec1[self.inx],
                                            num2=self.vec2[self.inx])

                elif data_type == list:
                    attr_freq = frequency[attr]
                    attr_domain = domain_size[attr]
                    self.set_distance(attr_name=attr, frequency=attr_freq, domain_size=attr_domain)
                self.inx += 1
        self.inx = self.inx - 1
        # print()

    def calc_distance(self):
        domain = read_domain_per_attr_data()
        freq = read_freq_per_value_data()

        for raw_data_inx, data_type in DATA_TYPE_PER_INDEX.items():
            attr = ATTRIBUTE_PER_INDEX[raw_data_inx]
            attr_freq = freq[attr]
            attr_domain = domain[attr]

            if data_type == str:
                self.categorical_distance(representation_option=self.representation_option, attr_type=data_type,
                                          frequency=attr_freq, domain_size=attr_domain)

            elif data_type == float or data_type == int:
                self.numerical_distance(representation_option=self.representation_option, attr_type=data_type,
                                        num1=self.vec1[self.inx],
                                        num2=self.vec2[self.inx])

            elif data_type == list:
                self.set_distance(attr_name=attr, frequency=attr_freq, domain_size=attr_domain)

            elif data_type == dict:
                self.nested_distance(attr_name=attr, frequency=attr_freq, domain_size=attr_domain)

            self.inx += 1

        # print(f'categorical result-\n {self.cat_distance_result}')
        # print(f'categorical list length-\n {len(self.cat_distance_result)}')
        # print(f'numerical result-\n {self.num_distance_result}')
        return q14(categorical_sum=sum(self.cat_distance_result),
                   numerical_sum=sum(self.num_distance_result))
        # print(f'distance result-\n {self.freq_distance_result}')
        # return self.freq_distance_result


def run_distance(vec1: list, vec2: list, representation_option: DistMethod, representation_option_set: DistMethod):
    return DistanceFlow(vec1=vec1, vec2=vec2, representation_option=representation_option,
                        representation_option_set=representation_option_set).calc_distance()


if __name__ == '__main__':
    instance1_ = {'laura gao': ('twitter',
                                [1, 1, 1, 5, 1996.0, 57, 14, 1, 7, 7, 1, 61, 61, 4, 1, 1, 1, 1, 14, 10, 7, 1, 1, 1, 68,
                                 1, 2013, 5, 4, 1, 709, 1, 650, 658, 1, 44, 117, 2, 233, 2, 1994, 165, 5, 8, 709, 11,
                                 650, 658, 1, 491, 117, 1, 170, 1, 2010, 2, 14, 14, 709, 4, 650, 658, 1, 179, 117, 91,
                                 170, 91, 2006, 165, 92, 7, 98, 156, 650, 658, 1, 44, 1, 1, 1, 1, None, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1, 1, 35, 58, 100, None, 104, 1, 1, 2, 42, 1, 100, None, 1, 1, 1, 1, 225,
                                 8, 11, 3.64, 104, 2, 1])}
    instance2_ = {'bruk argaw': ('twitter',
                                 [1, 1, 1, 93, 1991.0, 1, 14, 18, 88, 82, 1, 61, 61, 1, 34, 28, 22, 10, 14, 11, 10, 6,
                                  1, 1, 26, 1, 1916, 76, 6, 4, 709, 25, 650, 658, 1, 52, 1, 5, 233, 5, 1868, 76, 14, 4,
                                  709, 5, 650, 658, 1, 52, 1, 5, 233, 5, 1868, 76, 5, 11, 709, 5, 650, 658, 1, 52, 1,
                                  91, 170, 91, 2006, 165, 92, 1, 98, 156, 650, 658, 72, 491, 1, 1, 82, 1, 2016, 3, 3, 6,
                                  709, 156, 650, 658, 72, 491, 1, 1, 225, 58, 100, None, 1, 1, 1, 1, 225, 58, 3, None,
                                  1, 7, 1, 1, 42, 21, 100, None, 1, 1, 1])}

    vec1_ = [1, 1, 1, 144, 1993.0, 1, 826, 145, 668, 544, 1, 84, 84, 10, 87, 8, 1, 1, 502, 353, 303, 299, 94, 1, 215, 1,
             2001.0, 1336, 26, 38, 6047, 3, 5722, 5767, 1, 3304, 1, 164, 3178, 164, 1976.0, 231, 981, 26, 919, 169,
             5722, 5767, 480, 3304, 1, 1, 3178, 1, None, 93, 46, 99, 6047, 758, 758, 758, 14, 3304, 767, 4, 280, 4,
             1857.0, 587, 40, 21, 6047, 361, 5722, 5767, 6, 1613, 1, 1, 632, 1, 1997.0, 93, 35, 65, 6047, 5, 5722, 5767,
             98, 3304, 767, 3, 2354, 126, 122, None, 1022, 1, 1, 1, 255, 645, 1053, None, 1, 1, 1, 1, 2354, 645, 1053,
             None, 1, 1, 1]

    vec2_ = [1, 4, 2, 775, 1970.0, 1, 69, 127, 668, 544, 284, 84, 84, 15, 31, 8, 1, 1, 353, 299, 180, 110, 35, 164,
             3178, 164, 1976.0, 231, 23, 22, 919, 169, 5722, 5767, 308, 3304, 1083, 1, 365, 1, 2006.0, 901, 76, 65,
             6047, 1, 2, 258, 98, 3304, 767, 129, 3178, 129, 2004.0, 1206, 981, 13, 6047, 159, 5722, 5767, 308, 3304,
             1083, 1, 3178, 1, 2009.0, 87, 42, 62, 6047, 1, 81, 258, 1, 3304, 1, 164, 3178, 164, 1976.0, 231, 79, 52,
             6047, 169, 5722, 5767, 98, 3304, 767, 1, 2354, 645, 1053, None, 1, 1, 1, 17, 2354, 126, 83, None, 1, 1, 1,
             10, 2354, 126, 83, None, 1, 1, 1]

    run_distance(vec1=vec1_, vec2=vec2_, representation_option=DistMethod.fix_length_freq,
                 representation_option_set=DistMethod.fix_length_freq)
