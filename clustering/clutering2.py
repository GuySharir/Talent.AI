# For plotting
import matplotlib.pyplot as plt
# for matrix math
import numpy as np
# for normalization + probability density function computation
from scipy import stats
# for plotting
import seaborn as sns
from math import sqrt, log, exp, pi
from random import uniform
import pandas as pd

sns.set_style("white")


def load_mock_data() -> pd.DataFrame:
    random_seed = 17
    np.random.seed(random_seed)
    df = pd.DataFrame(data=np.random.rand(100))
    return df


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def display_data(data: pd.DataFrame) -> None:
    sns.histplot(data, bins=20)
    # sns.distplot(data, bins=20, kde=False)
    plt.show()


class Gaussian:
    "Model univariate Gaussian"

    def __init__(self, mu, sigma):
        # mean and standard deviation
        self.mu = mu
        self.sigma = sigma

    # probability density function
    def pdf(self, datum):
        "Probability of a data point given the current parameters"
        u = (datum - self.mu) / abs(self.sigma)
        y = (1 / (sqrt(2 * pi) * abs(self.sigma))) * exp(-u * u / 2)
        return y

    # printing model values
    def __repr__(self):
        return 'Gaussian({0:4.6}, {1:4.6})'.format(self.mu, self.sigma)


class GaussianMixture:
    "Model mixture of two univariate Gaussians and their EM estimation"

    def __init__(self, data, sigma_min=.1, sigma_max=1, mix=.5):
        self.loglike = 0
        self.data = data
        mu_min = min(data)
        mu_max = max(data)
        # init with multiple gaussians
        self.one = Gaussian(uniform(mu_min, mu_max),
                            uniform(sigma_min, sigma_max))
        self.two = Gaussian(uniform(mu_min, mu_max),
                            uniform(sigma_min, sigma_max))

        # as well as how much to mix them
        self.mix = mix

    def Estep(self):
        "Perform an E(stimation)-step, freshening up self.loglike in the process"
        # compute weights
        self.loglike = 0.  # = log(p = 1)
        for datum in self.data:
            # unnormalized weights
            wp1 = self.one.pdf(datum) * self.mix
            wp2 = self.two.pdf(datum) * (1. - self.mix)
            # compute denominator
            den = wp1 + wp2
            # normalize
            wp1 /= den
            wp2 /= den
            # add into loglike
            self.loglike += log(wp1 + wp2)
            # yield weight tuple
            yield (wp1, wp2)

    def Mstep(self, weights):
        "Perform an M(aximization)-step"
        # compute denominators
        (left, rigt) = zip(*weights)
        one_den = sum(left)
        two_den = sum(rigt)
        # compute new means
        self.one.mu = sum(w * d / one_den for (w, d) in zip(left, self.data))
        self.two.mu = sum(w * d / two_den for (w, d) in zip(rigt, self.data))
        # compute new sigmas
        self.one.sigma = sqrt(sum(w * ((d - self.one.mu) ** 2)
                                  for (w, d) in zip(left, self.data)) / one_den)
        self.two.sigma = sqrt(sum(w * ((d - self.two.mu) ** 2)
                                  for (w, d) in zip(rigt, self.data)) / two_den)
        # compute new mix
        self.mix = one_den / len(self.data)

    def iterate(self, N=1, verbose=False):
        "Perform N iterations, then compute log-likelihood"

    def pdf(self, x):
        return (self.mix) * self.one.pdf(x) + (1 - self.mix) * self.two.pdf(x)

    def __repr__(self):
        return 'GaussianMixture({0}, {1}, mix={2.03})'.format(self.one,
                                                              self.two,
                                                              self.mix)

    def __str__(self):
        return 'Mixture: {0}, {1}, mix={2:.03})'.format(self.one,
                                                        self.two,
                                                        self.mix)


data = load_mock_data()
# display_data(data)

n_iterations = 20
n_random_restarts = 500
best_mix = None
best_loglike = float('-inf')
print('Computing best model with random restarts...\n')
for _ in range(n_random_restarts):
    mix = GaussianMixture(data)
    for _ in range(n_iterations):
        try:
            mix.iterate()
            if mix.loglike > best_loglike:
                best_loglike = mix.loglike
                best_mix = mix
        except (ZeroDivisionError, ValueError,
                RuntimeWarning):  # Catch division errors from bad starts, and just throw them out...
            pass
print('\n\nDone. 🙂')

x = np.linspace(0, 1, 100)

sns.distplot(data, bins=20, kde=False, norm_hist=True)
g_both = [best_mix.pdf(e) for e in x]
plt.plot(x, g_both, label='gaussian mixture');
plt.legend()
plt.show()
