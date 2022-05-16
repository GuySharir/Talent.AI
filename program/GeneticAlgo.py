# number of input values - 1 = z
# number of parameters (weights) - 4 = theta1, theta2, beta, gama

# z represents the domain size that is per attribute
class GeneticAlg:
    def __init__(self):
        self.theta1 = None
        self.theta2 = None
        self.beta = None
        self.gama = None
        self.z = None

    def func(self) -> float:
        if self.z <= self.theta1:
            return 1
        elif self.theta1 < self.z <= self.theta2:
            return 1 - self.beta * (self.z - self.theta1)
        elif self.theta2 < self.z:
            return 1 - self.beta * (self.theta2 - self.theta1) - self.gama * (self.z - self.theta2)

    def genetic_per_attribute(self, attr):
        # read domain value according to the given attribute (from domain size file)
        self.z = attr