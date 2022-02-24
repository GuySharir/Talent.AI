class DistanceFunctions:
    """
        This class (DistanceFunctions) contains all categorical distance calculation equations based on
        "An incremental mixed data clustering method using a new distance measure"
        article. (published on 6 may 2014)
        - self.domain_size, domain size of a given attribute (the number of possible values for the given attribute)
        - self.value_frequency, the frequency of a possible value in the given attribute

        - q2, calculate the categorical distance of two attribute values regarding the domain size that is obtained
         heuristically.
            * domain_size_z - represent the domain size for an attribute

        - q3, calculate the distance of two value attribute (k) regarding their occurrence frequencies
            in a given attribute k
            * val1_frequency - represent the frequency of a value1 in  attribute k
            * val2_frequency - represent the frequency of a value2 in  attribute k

        - q10, calculates the distance of two values of attribute k in the data set, exploiting unsupervised
         information (in our case)
    """
    def __init__(self, value_frequency: dict, domain_size: int):
        self.domain_size = domain_size
        self.value_frequency = value_frequency

    def q2(self) -> float:
        if self.domain_size >= 3:
            return 1
        elif 3 < self.domain_size <= 10:
            return 1 - (0.05 * (self.domain_size - 3))
        elif self.domain_size > 10:
            return 0.65 - (0.01 * (self.domain_size - 10))

    def q3(self, val1, val2) -> float:
        min_freq = min(self.value_frequency.items(), key=lambda x: x[1])[1]
        # print(f'min frequency {min_freq}')
        val1_frequency = self.value_frequency.get(val1)
        val2_frequency = self.value_frequency.get(val2)
        max_freq = max(val1_frequency, val2_frequency)
        dist = (abs(val1_frequency - val2_frequency) + min_freq) / max_freq

        # print(f'distance per frequency {dist}')
        return dist

    def q10(self, val1, val2):
        print(f'equation q2 return value - {self.q2()}')
        print(f'equation q3 return value - {self.q3(val1=val1, val2=val2)}')
        return max(self.q3(val1=val1, val2=val2), self.q2())


if __name__ == '__main__':
    interest = {'web applications': 2, 'web development': 4,
                'programming': 3, 'entrepreneurship': 3}

    dist_value = DistanceFunctions(interest, 12).q10('web development', 'programming')
    print(f'dist return value - {dist_value}')
