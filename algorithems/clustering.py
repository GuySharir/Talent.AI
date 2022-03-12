# import libraries

# For plotting
import math
import random
import json

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

# x = np.linspace(0, 1, 100)  # to plot the data


#
# tmp = []
# max_val = 0
# min_val = 10000
#
# for key in res.keys():
#     total = sum(res[key])
#     tmp.append(res[key])
#
#     if total > max_val:
#         max_val = total
#     if total < min_val:
#         min_val = total
# print(f"sum: {key} - {total}")
# print(f"max: {key} - {max(res[key])}")
# print(f"min: {key} - {min(res[key])}")
# print(f"unique: {key} - {len(np.unique(res[key]))}\n")

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 100)

# y = pd.read_csv('../program/foo.csv')
# print(y.describe(include='all'))

# data = []
# for val in tmp:
#     data.append((val - min_val) / (max_val - min_val))

# sns.displot(res["george lo"], bins=100, kde=False);
# # # sns.displot(res.values(), bins=100, kde=False);
# # # sns.kdeplot(tmp)
# plt.show()

from sklearn.mixture import GaussianMixture

data = None

data = np.load('../program/full_matrix.npy')
# print(data)

# print(len(np.unique(data)))

train = data[0:60]
test = data[61:-1]

# sns.displot(data, bins=100)
# sns.heatmap(data)
# sns.scatterplot(data=data, )
# plt.show()

for i in range(1, 10):
    gmm = GaussianMixture(n_components=i, tol=0.00000001, max_iter=500)
    gmm.fit(train)  # Parameters: array-like, shape (n_samples, n_features), 1 dimension dataset so 1 feature

    print(f"\nnow running example with {i} gaussians\n")
    print(gmm.aic(test))
    print(gmm.bic(test))
    print(gmm.predict(test))
    print("**************************************")

# print(gmm.means_)

# # print('Input Gaussian {:}: μ = {:.2}, σ = {:.2}'.format("1", Mean1, Standard_dev1))
# # print('Input Gaussian {:}: μ = {:.2}, σ = {:.2}'.format("2", Mean2, Standard_dev2))
# Gaussian_nr = 1
# for mu, sd, p in zip(gmm.means_.flatten(), np.sqrt(gmm.covariances_.flatten()), gmm.weights_):
#     print('Gaussian {:}: μ = {:.2}, σ = {:.2}, weight = {:.2}'.format(Gaussian_nr, mu, sd, p))
#     g_s = stats.norm(mu, sd).pdf(x) * p
#     plt.plot(x, g_s, label=f'gaussian {Gaussian_nr} sklearn');
#     Gaussian_nr += 1
# #
# sns.distplot(data, bins=20, kde=False, norm_hist=True)
# gmm_sum = np.exp(
#     [gmm.score_samples(e.reshape(-1, 1)) for e in x])  # gmm gives log probability, hence the exp() function
# plt.plot(x, gmm_sum, label='gaussian mixture');
# plt.legend()
# plt.show()

# print(gmm.means_)
