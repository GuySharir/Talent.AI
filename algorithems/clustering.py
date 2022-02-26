# import libraries

# For plotting
import random

import matplotlib.pyplot as plt
import numpy
import seaborn as sns

sns.set_style("white")
# %matplotlib inline
# for matrix math
import numpy as np
# for normalization + probability density function computation
from scipy import stats
# for data preprocessing
import pandas as pd
from math import sqrt, log, exp, pi
from random import uniform

x = np.linspace(0, 1, 100)  # to plot the data

# sns.displot(data, bins=20, kde=False);
# plt.show()

SIZE = 1000
data = numpy.zeros((SIZE, SIZE))

random_seed = 17
np.random.seed(random_seed)

r = []

for i in range(SIZE):
    for j in range(i + 1, SIZE):
        tmp = np.random.rand(1)
        data[i][j] = tmp
        data[j][i] = tmp

# data = pd.DataFrame(data)

# data = pd.DataFrame(data=np.random.rand(10, 2), columns=["x", "y"])
# data = np.random.rand(5, 5)
sns.distplot([sum(x) for x in data], kde=False, bins=100)

# print(data)
# sns.scatterplot(data=data,)
plt.show()

for row in data:
    print(sum(row))

# from sklearn.mixture import GaussianMixture
#
# gmm = GaussianMixture(n_components=5, tol=0.000001)
# gmm.fit(
#     np.expand_dims(data, 1))  # Parameters: array-like, shape (n_samples, n_features), 1 dimension dataset so 1 feature
# Gaussian_nr = 1
# # print('Input Gaussian {:}: μ = {:.2}, σ = {:.2}'.format("1", Mean1, Standard_dev1))
# # print('Input Gaussian {:}: μ = {:.2}, σ = {:.2}'.format("2", Mean2, Standard_dev2))
# for mu, sd, p in zip(gmm.means_.flatten(), np.sqrt(gmm.covariances_.flatten()), gmm.weights_):
#     print('Gaussian {:}: μ = {:.2}, σ = {:.2}, weight = {:.2}'.format(Gaussian_nr, mu, sd, p))
#     g_s = stats.norm(mu, sd).pdf(x) * p
#     plt.plot(x, g_s, label=f'gaussian {Gaussian_nr} sklearn');
#     Gaussian_nr += 1
#
# sns.distplot(data, bins=20, kde=False, norm_hist=True)
# gmm_sum = np.exp(
#     [gmm.score_samples(e.reshape(-1, 1)) for e in x])  # gmm gives log probability, hence the exp() function
# plt.plot(x, gmm_sum, label='gaussian mixture');
# plt.legend()
# plt.show()

# print(gmm.means_)
