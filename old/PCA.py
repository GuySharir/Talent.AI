import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import json

# data = None
#
# data = np.load('../programFlow/full_matrix.npy')
# data = pd.DataFrame(data)
#
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(data.describe())
#
# # x = StandardScaler().fit_transform(data)
# # # x = pd.DataFrame(x)
# #
# # pca = PCA(n_components=1)
# # principalComponents = pca.fit_transform(x)
# # principalDf = pd.DataFrame(data=principalComponents
# #                            , columns=['principal component 1'])
# #
# # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
# #     print(principalDf)
# #
# # sns.displot(data=principalDf, bins=200)
# # plt.show()
