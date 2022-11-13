import json
import math

from program.ReadData import read_freq_per_value_data, read_domain_per_attr_data, DATA_TYPE_PER_INDEX, \
    ATTRIBUTE_PER_INDEX, DATA_TYPE_PER_INDEX_EXPERIENCE, DATA_TYPE_PER_INDEX_EDUCATION,\
    EXPERIENCE_ATTRIBUTE_PER_INDEX, EDUCATION_ATTRIBUTE_PER_INDEX, HAMMING_DEFAULT, \
    ONE_HOT_SPARE, set_path

from dataTool.runtimeObjectsInfo.ListLengthData import LIST_LENGTH_PER_ATTR, NESTED_LENGTH_PER_ATTR
from program.DistEnum import DistMethod
from program.DistFunctions import DistanceData, q14, categorical_dist_between_freq_vectors, \
    numerical_dist_between_freq_vectors
import numpy as np


def logger(*args):
    # print(*args)
    pass


class DistanceFlowFreq:
    def __init__(self, vec1: list, vec2: list, representation_option: DistMethod, representation_option_set: DistMethod,
                 one_hot_inx_flag: bool = False, t1: int = 3, t2: int = 10, beta: float = 0.05, gama: float = 0.01):
        self.vec1 = vec1
        self.vec2 = vec2
        self.inx = 0

        self.representation_option = representation_option
        self.representation_option_set = representation_option_set

        self.cat_distance_result = []
        self.num_distance_result = []

        self.one_hot_index = set_path('dataTool/one_hot_index.json')
        self.one_hot_inx_flag = one_hot_inx_flag
        self.one_hot_index_list = []

        # genetic alg parameters
        self.t1, self.t2, self.beta, self.gama = t1, t2, beta, gama

    def write_inx_of_one_hot_vector(self, domain_size: int):
        index = self.inx
        if self.representation_option_set == DistMethod.inner_product or self.representation_option_set == DistMethod.intersection:
            for _ in range(domain_size + ONE_HOT_SPARE):
                self.one_hot_index_list.append(index)
                index += 1

        with open(self.one_hot_index, 'w') as fp:
            json.dump(self.one_hot_index_list, fp)

    def numerical_distance(self, representation_option: DistMethod, attr_type, num1, num2):
        # dealing with missing values when numerical type by deleting missing data
        if num1 and num2:
            if representation_option == DistMethod.fix_length_freq:
                self.num_distance_result.append(numerical_dist_between_freq_vectors(attr_type=attr_type,
                                                                                    num_val1=num1, num_val2=num2))
            elif representation_option == DistMethod.hamming_distance:
                if self.vec1[self.inx] != HAMMING_DEFAULT and self.vec2[self.inx] != HAMMING_DEFAULT:
                    self.num_distance_result.append(np.sqrt((num1 - num2) ** 2))

    def categorical_distance(self, representation_option: DistMethod, attr_type, frequency: dict, domain_size: int):

        if representation_option == DistMethod.fix_length_freq:
            data = DistanceData(instance1=self.vec1, instance2=self.vec2, val1_frequency=self.vec1[self.inx],
                                val2_frequency=self.vec2[self.inx], frequency=frequency,
                                domain_size=domain_size, attribute_inx=self.inx,
                                t1=self.t1, t2=self.t2, beta=self.beta, gama=self.gama)
            result = categorical_dist_between_freq_vectors(attr_type=attr_type, data=data)

            self.cat_distance_result.append(result)

        elif representation_option == DistMethod.hamming_distance:
            if self.vec1[self.inx] != HAMMING_DEFAULT and self.vec2[self.inx] != HAMMING_DEFAULT:
                if self.vec1[self.inx] == self.vec2[self.inx]:
                    self.cat_distance_result.append(0)
                else:
                    self.cat_distance_result.append(1)

    def set_distance(self, attr_name: str, frequency: dict, domain_size: int):
        # each set contains only categorical values in different representations

        if self.representation_option_set == DistMethod.fix_length_freq or self.representation_option_set == DistMethod.hamming_distance:
            attr_length = LIST_LENGTH_PER_ATTR[attr_name]
            # set1 = self.vec1[self.inx: self.inx + attr_length]
            # set2 = self.vec2[self.inx: self.inx + attr_length]

            for _ in range(attr_length):
                self.categorical_distance(representation_option=self.representation_option_set, attr_type=str,
                                          frequency=frequency, domain_size=domain_size)
                self.inx += 1

        elif self.representation_option_set == DistMethod.inner_product or self.representation_option_set == DistMethod.intersection:
            # set1 = self.vec1[self.inx: self.inx + (domain_size + ONE_HOT_SPARE)]
            # set2 = self.vec2[self.inx: self.inx + (domain_size + ONE_HOT_SPARE)]

            if self.representation_option_set == DistMethod.intersection:
                if self.one_hot_inx_flag:
                    self.write_inx_of_one_hot_vector(domain_size=domain_size)
                union_or_count = 0
                inner_product_sum = 0
                for _ in range(domain_size + ONE_HOT_SPARE):
                    inner_product_sum += self.vec1[self.inx] * self.vec2[self.inx]
                    if self.vec1[self.inx] == 1 or self.vec2[self.inx] == 1:
                        union_or_count += 1
                    self.inx += 1
                if not union_or_count:
                    self.cat_distance_result.append(1 - inner_product_sum)
                else:
                    self.cat_distance_result.append(1 - (inner_product_sum / union_or_count))

            elif self.representation_option_set == DistMethod.inner_product:
                if self.one_hot_inx_flag:
                    self.write_inx_of_one_hot_vector(domain_size=domain_size)
                inner_product_sum = 0
                vec1_p = 0
                vec2_q = 0
                for _ in range(domain_size + ONE_HOT_SPARE):
                # for _ in range(domain_size):
                    inner_product_sum += self.vec1[self.inx] * self.vec2[self.inx]
                    vec1_p += pow(self.vec1[self.inx], 2)
                    vec2_q += pow(self.vec2[self.inx], 2)
                    self.inx += 1
                inner_product_res = vec1_p + vec2_q - (2 * inner_product_sum)
                # math.sqrt(inner_product_res)
                self.cat_distance_result.append(math.sqrt(inner_product_res))
                # self.cat_distance_result.append(1 - inner_product_sum)
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
                    # self.first_one_hot_inx = self.inx
                    self.set_distance(attr_name=attr, frequency=attr_freq, domain_size=attr_domain)
                    # self.last_one_hot_inx = self.inx
                    # self.write_inx_of_one_hot_vector()
                self.inx += 1
        self.inx = self.inx - 1
        # print()

    def calc_distance(self, birth_year: bool = True, gender: bool = True) -> float:
        domain = read_domain_per_attr_data()
        freq = read_freq_per_value_data()

        for raw_data_inx, data_type in DATA_TYPE_PER_INDEX.items():
            attr = ATTRIBUTE_PER_INDEX[raw_data_inx]
            attr_freq = freq[attr]
            attr_domain = domain[attr]

            if data_type == str:
                if attr == 'gender' and not gender:
                    pass
                else:
                    self.categorical_distance(representation_option=self.representation_option, attr_type=data_type,
                                              frequency=attr_freq, domain_size=attr_domain)

            elif data_type == float or data_type == int:
                if attr == 'birth_year' and not birth_year:
                    pass
                else:
                    self.numerical_distance(representation_option=self.representation_option, attr_type=data_type,
                                            num1=self.vec1[self.inx],
                                            num2=self.vec2[self.inx])

            elif data_type == list:
                self.set_distance(attr_name=attr, frequency=attr_freq, domain_size=attr_domain)

            elif data_type == dict:
                self.nested_distance(attr_name=attr, frequency=attr_freq, domain_size=attr_domain)

            self.inx += 1

        if self.representation_option == DistMethod.hamming_distance:
            hamming_result = np.sqrt((sum(self.cat_distance_result) - sum(self.num_distance_result)) ** 2)
            return hamming_result
        else:
            freq_distance_result = q14(categorical_sum=sum(self.cat_distance_result),
                                       numerical_sum=sum(self.num_distance_result))
            return freq_distance_result


def run_distance_freq(vec1: list, vec2: list, representation_option: DistMethod, representation_option_set: DistMethod,
                      birth_year: bool = True, gender: bool = True, one_hot_inx_flag: bool = False,
                      t1: int = 3, t2: int = 10, beta: float = 0.05, gama: float = 0.01) -> float:
    return DistanceFlowFreq(vec1=vec1, vec2=vec2, representation_option=representation_option,
                            representation_option_set=representation_option_set,
                            one_hot_inx_flag=one_hot_inx_flag, t1=t1, t2=t2, beta=beta, gama=gama).calc_distance(birth_year=birth_year, gender=gender)


# different distance options
def freq_rep_dist(vec1: list, vec2: list, birth_year: bool = True, gender: bool = True,
                  t1: int = 3, t2: int = 10, beta: float = 0.05, gama: float = 0.01) -> float:
    return run_distance_freq(vec1=vec1, vec2=vec2, representation_option=DistMethod.fix_length_freq,
                             representation_option_set=DistMethod.fix_length_freq, birth_year=birth_year, gender=gender,
                             t1=t1, t2=t2, beta=beta, gama=gama)


def hamming_rep_dist(vec1: list, vec2: list, birth_year: bool = True, gender: bool = True) -> float:
    return run_distance_freq(vec1=vec1, vec2=vec2, representation_option=DistMethod.hamming_distance,
                             representation_option_set=DistMethod.hamming_distance, birth_year=birth_year,
                             gender=gender)


def inner_product_rep_dist(vec1: list, vec2: list, birth_year: bool = True, gender: bool = True,
                           one_hot_inx_flag: bool = False) -> float:
    return run_distance_freq(vec1=vec1, vec2=vec2, representation_option=DistMethod.fix_length_freq,
                             representation_option_set=DistMethod.inner_product, birth_year=birth_year, gender=gender,
                             one_hot_inx_flag=one_hot_inx_flag)


def intersection_rep_dist(vec1: list, vec2: list, birth_year: bool = True, gender: bool = True,
                          one_hot_inx_flag: bool = False) -> float:
    return run_distance_freq(vec1=vec1, vec2=vec2, representation_option=DistMethod.fix_length_freq,
                             representation_option_set=DistMethod.intersection, birth_year=birth_year, gender=gender,
                             one_hot_inx_flag=one_hot_inx_flag)


if __name__ == '__main__':
    # option 1
    freq_vec1_ = [1, 1, 1, 5, 1996.0, 57, 14, 1, 7, 7, 1, 61, 61, 4, 1, 1, 1, 1, 14, 10, 7, 1, 1, 1, 68, 1, 2013, 5, 4,
                  1,
                  709, 1, 650, 658, 1, 44, 117, 2, 233, 2, 1994, 165, 5, 8, 709, 11, 650, 658, 1, 491, 117, 1, 170, 1,
                  2010,
                  2, 14, 14, 709, 4, 650, 658, 1, 179, 117, 91, 170, 91, 2006, 165, 92, 7, 98, 156, 650, 658, 1, 44, 1,
                  1, 1,
                  1, None, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 35, 58, 100, None, 104, 1, 1, 2, 42, 1, 100, None, 1, 1, 1,
                  1,
                  225, 8, 11, 3.64, 104, 2, 1]
    freq_vec2_ = [1, 1, 1, 93, 1991.0, 1, 14, 18, 88, 82, 1, 61, 61, 1, 34, 28, 22, 10, 14, 11, 10, 6, 1, 1, 26, 1,
                  1916, 76,
                  6, 4, 709, 25, 650, 658, 1, 52, 1, 5, 233, 5, 1868, 76, 14, 4, 709, 5, 650, 658, 1, 52, 1, 5, 233, 5,
                  1868,
                  76, 5, 11, 709, 5, 650, 658, 1, 52, 1, 91, 170, 91, 2006, 165, 92, 1, 98, 156, 650, 658, 72, 491, 1,
                  1, 82,
                  1, 2016, 3, 3, 6, 709, 156, 650, 658, 72, 491, 1, 1, 225, 58, 100, None, 1, 1, 1, 1, 225, 58, 3, None,
                  1,
                  7, 1, 1, 42, 21, 100, None, 1, 1, 1]
    # freq_rep_dist(vec1=freq_vec1_, vec2=freq_vec2_, birth_year=True, gender=True)

    # option 2
    hamming_vec1_ = ['laura gao', 'laura', 'gao', 'female', 1996.0, None, 'internet', 'associate product manager ii',
                     'operations', 'product', '$', 'twitter', 'twitter', '2018-09', 'potenciamiento económico', '$',
                     '$', '$',
                     'public speaking', 'management', 'microsoft office', 'technology', 'creative strategy',
                     'smartypal',
                     '1-10', 'smartypal', 2013, 'e-learning', '2017', '2017', False,
                     'philadelphia, pennsylvania, united states', 'united states', 'north america',
                     'product management intern',
                     'operations', 'training', 'amazon', '10001+', 'amazon', 1994, 'internet', '2017-08', '2017-06',
                     False,
                     'seattle, washington, united states', 'united states', 'north america',
                     'business data analyst intern',
                     'engineering', 'training', 'consumer financial protection bureau', '1001-5000',
                     'consumer-financial-protection-bureau', 2010, 'government administration', '2015-08', '2015-06',
                     False,
                     'washington, district of columbia, united states', 'united states', 'north america',
                     'chief of staff policy intern', None, 'training', 'twitter', '1001-5000', 'twitter', 2006,
                     'internet',
                     None, '2018-09', True, 'san francisco, california, united states', 'united states',
                     'north america',
                     'associate product manager ii', 'operations', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$',
                     '$', '$',
                     '$', '$', '$', 'graduate school of city planning minor', None, None, None, None, 'bachelors', '$',
                     '$',
                     'coppell high school', 'secondary school', '2014-05', None, None, '$', '$', '$',
                     'the wharton school',
                     'post-secondary institution', '2018', '2014', 3.64, 'bachelors', 'economics', '$']

    hamming_vec2_ = ['bruk argaw', 'bruk', 'argaw', 'male', 1991.0, '1991-01-23', 'internet', 'software engineer',
                     'engineering', 'software', '$', 'twitter', 'twitter', '2020-03', 'environment', 'education',
                     'poverty alleviation', 'science and technology', 'matlab', 'engineering', 'microsoft excel',
                     'microsoft word', 'research', 'sacramento city college', '501-1000', 'sacramento-city-college',
                     1916,
                     'higher education', '2013-04', '2013-01', False, 'united states', 'united states', 'north america',
                     'lab ta', 'education', '$', 'uc berkeley', '10001+', 'uc-berkeley', 1868, 'higher education',
                     '2015-08',
                     '2015-05', False, 'berkeley, california, united states', 'united states', 'north america',
                     'research assistant @ pavement research center', 'education', '$', 'uc berkeley', '10001+',
                     'uc-berkeley',
                     1868, 'higher education', '2014-04', '2014-01', False, 'berkeley, california, united states',
                     'united states', 'north america', 'research assistant @ davis labs', 'education', '$', 'twitter',
                     '1001-5000', 'twitter', 2006, 'internet', None, '2020-03', True,
                     'san francisco, california, united states', 'united states', 'north america', 'software engineer',
                     'engineering', '$', 'indio technologies inc.', '51-200', 'indiotechnologies', 2016, 'insurance',
                     '2019-05',
                     '2017-08', False, 'san francisco, california, united states', 'united states', 'north america',
                     'software engineer', 'engineering', '$', 'sacramento city college', 'post-secondary institution',
                     None,
                     None, None, '$', '$', '$', 'app academy', 'post-secondary institution', None, '2017', None, '$',
                     'software engineering', '$', 'el camino fundamental high school', 'secondary school', '2010', None,
                     None,
                     '$', '$', '$']
    # hamming_rep_dist(vec1=hamming_vec1_, vec2=hamming_vec2_, birth_year=True, gender=True)

    # option 3 and 4
    # option 3
    one_hot_vec1_ = [1, 1, 1, 93, 1995.0, 57, 84, 1, 88, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 37, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 170, 2, 2013, 68, 3, 6, 709, 156, 650, 658, 1, 179, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 62, 233, 62, 2003, 68, 92, 1, 98, 78, 650, 658, 1, 491, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 170, 2, 2013, 68, 1, 2, 709, 156, 650, 658, 1, 52, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 70, 70, None, 78, 7, 2, 709, 90, 90, 90, 1, 179, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 68, 1, None, 6, 3, 8, 709, 1, 650, 658, 1, 179, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 42, 17, 17, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 225, 8, 7, None, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    one_hot_vec2_ = [1, 1, 1, 93, 1956.0, 57, 84, 1, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 37, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 70, 70, None, 78, 9, 8, 709, 90, 90, 90, 72, 491, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 233, 1, 1977, 72, 1, 1, 709, 1, 650, 658, 1, 179, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 70, 70, None, 78, 6, 5, 709, 90, 90, 90, 1, 179, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 62, 233, 62, 2003, 68, 2, 7, 98, 78, 650, 658, 1, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 233, 1, 1967, 8, 1, 1, 709, 5, 650, 658, 1, 491, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 42, 58, 100, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 225, 19, 4, None, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 225, 58, 13, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    inner_product_rep_dist(vec1=one_hot_vec1_, vec2=one_hot_vec2_, birth_year=False, gender=True, one_hot_inx_flag=True)

    # option 4
    # intersection_rep_dist(vec1=one_hot_vec1_, vec2=one_hot_vec2_, birth_year=False, gender=True, one_hot_inx_flag=True)
