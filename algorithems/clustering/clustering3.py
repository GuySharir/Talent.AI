import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.utils import shuffle

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 80)
pd.set_option('display.width', 100)


def SelBest(arr: list, X: int) -> list:
    '''
    returns the set of X configurations with shorter distance
    '''
    dx = np.argsort(arr)[:X]
    return arr[dx]


SelBest = lambda arr, x: arr[np.argsort(arr)[:x]]

# def normalize(df: DataFrame):
#     abs_max = 0
#     abs_min = 1000
#
#     for row in df.iterrows():
#         cur_max = max(row)
#         cur_min = min(row)


# raw_df = np.load('../../program/combined3.npy')
raw_df = np.load('combined3.npy')
raw_df = pd.DataFrame(raw_df)
raw_df = shuffle(raw_df)

# Standardize data
scaler = StandardScaler()
scaled_df = scaler.fit_transform(raw_df)

# Normalizing the Data
normalized_df = normalize(scaled_df)

# Converting the numpy array into a pandas DataFrame
normalized_df = pd.DataFrame(normalized_df)

# Reducing the dimensions of the data
pca = PCA(n_components=2)
X_principal = pca.fit_transform(normalized_df)
X_principal = pd.DataFrame(X_principal)
X_principal.columns = ['P1', 'P2']

# plt.scatter(X_principal['P1'], X_principal['P2'],
#             c=GaussianMixture(n_components=5).fit_predict(X_principal), cmap=plt.cm.winter, alpha=0.6)
# plt.show()

print(np.shape(raw_df))

n_clusters = np.arange(2, 16)
sils = []
sils_err = []
iterations = 20
for n in n_clusters:
    tmp_sil = []
    flag = True
    for _ in range(iterations):
        # gmm = GaussianMixture(n, n_init=2).fit(X_principal)
        kmeans = KMeans(n_clusters=n).fit(X_principal)
        # labels = gmm.predict(X_principal)
        labels = kmeans.predict(X_principal)
        sil = metrics.silhouette_score(X_principal, labels, metric='euclidean')
        tmp_sil.append(sil)
        if flag:
            plt.scatter(X_principal['P1'], X_principal['P2'], c=labels)
            plt.title(f"number of clusters: {n}")
            plt.show()
            flag = False

    val = np.mean(SelBest(np.array(tmp_sil), int(iterations / 5)))
    err = np.std(tmp_sil)
    sils.append(val)
    sils_err.append(err)
    flag = True

plt.errorbar(n_clusters, sils, yerr=sils_err)
plt.title("Silhouette Scores", fontsize=20)
plt.xticks(n_clusters)
plt.xlabel("N. of clusters")
plt.ylabel("Score")
plt.show()


class Classifier:

    def __init__(self, n_clusters):
        self.model = KMeans(n_clusters=n_clusters)

    def fit(self, data):
        self.model.fit(data)

    def get_model(self):
        return self.mo
