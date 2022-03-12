class DistanceStrFunctions:
    """
        - q2, calculate the categorical distance of two attribute values regarding the domain size that is obtained
         heuristically.
            * domain_size_z - represent the domain size for an attribute

        - q3, calculate the distance of two value attribute (k) regarding their occurrence frequencies
            in a given attribute k
            * val1_frequency - represent the frequency of a value1 in  attribute k
            * val2_frequency - represent the frequency of a value2 in  attribute k

        - q10, calculates the distance of two values of attribute k in the data set, exploiting unsupervised
         information (in our case)

        - calc_num_distance_q13,

    """

    @staticmethod
    def q2(domain_size: int) -> float:
        if domain_size >= 3:
            return 1
        elif 3 < domain_size <= 10:
            return 1 - (0.05 * (domain_size - 3))
        elif domain_size > 10:
            return 0.65 - (0.01 * (domain_size - 10))

    @staticmethod
    def q3(val1: str, val2: str, value_frequency: dict) -> float:
        if not val1:
            val1 = 'null'
        if not val2:
            val2 = 'null'

        min_freq = min(value_frequency.items(), key=lambda x: x[1])[1]
        print(f'min frequency {min_freq}')
        val1_frequency = value_frequency.get(val1)
        val2_frequency = value_frequency.get(val2)
        max_freq = max(val1_frequency, val2_frequency)
        dist = (abs(val1_frequency - val2_frequency) + min_freq) / max_freq

        return dist

    def q10(self, val1: str, val2: str, value_frequency: dict, domain_size: int) -> float:
        print(f'equation q2 return value - {self.q2(domain_size=domain_size)}')
        print(f'equation q3 return value - {self.q3(val1=val1, val2=val2, value_frequency=value_frequency)}')
        q3result = self.q3(val1=val1, val2=val2, value_frequency=value_frequency)
        q2result = self.q2(domain_size=domain_size)

        if not q3result and not q2result:
            return 0
        elif not q3result and q2result:
            return q2result
        elif q3result and not q2result:
            return q3result
        else:
            return max(q3result, q2result)

    @staticmethod
    def q12(attribute: str, instance_a: dict, instance_b: dict) -> int:
        if instance_a[attribute] == instance_b[attribute]:
            return 0
        elif instance_a[attribute] != instance_b[attribute]:
            return 1

    @staticmethod
    def calc_num_distance_q13(val1, val2) -> float:
        print(f'numeric {val1} , {val2}')
        if not val1 or not val2:
            return 0
        else:
            return (val1 - val2) ** 2


if __name__ == '__main__':
    pass


