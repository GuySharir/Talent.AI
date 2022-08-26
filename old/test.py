from datetime import datetime

import matplotlib.pyplot as plt

from program.DistanceFlow import freq_rep_dist
from kMeans import Kmeans
import numpy as np
import pandas as pd
import pickle as pkl
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, normalize, StandardScaler, Normalizer
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree


def create_matrix():
    with open('./five_my.pkl', 'rb') as inp:
        model: Kmeans = pkl.load(inp)

    data = model.data
    order = model.order

    size = len(data)
    print(model.data)

    distances = np.zeros((size, size))
    start = 0

    for i in range(size):
        if i == 0:
            start = datetime.now()
        if i == 1:
            now = datetime.now()
            diff = now - start
            print(f"total time to calculate will be: {diff.total_seconds() / 60 * size} minutes")

        print(f"now calculating the {i} row out of {size}")

        first = list(data.iloc[i])
        # print(first)

        for j in range(i, size):
            second = list(data.iloc[j])
            distances[i][j] = distances[j][i] = freq_rep_dist(first, second)

    with open('matrix.pkl', 'wb') as f:
        pkl.dump(distances, f)

    print(distances)


def reduce_dimension(data) -> pd.DataFrame:
    pca = PCA(n_components=2)
    x_principal = pca.fit_transform(data)
    x_principal = pd.DataFrame(x_principal)
    x_principal.columns = ['p1', 'p2']
    return x_principal


def scale_data(data, scaler_type: str) -> pd.DataFrame:
    transformer = Normalizer()
    data = transformer.transform(data)

    if scaler_type == "standard":
        scaler = StandardScaler()
        data = scaler.fit_transform(data)

    if scaler_type == "minmax":
        mms = MinMaxScaler()
        data = mms.fit_transform(data)

    return data


def means():
    #
    with open('./matrix.pkl', 'rb') as inp:
        x = pkl.load(inp)

    with open('./five_my.pkl', 'rb') as inp:
        old: Kmeans = pkl.load(inp)

    x = scale_data(x, 'standard')
    data = reduce_dimension(x)

    model = KMeans(n_clusters=7, random_state=0).fit(data)

    clusters = [[] for _ in range(7)]

    size = len(old.data)
    for idx in range(size):
        label = old.order.iloc[idx]['company']

        clusters[model.labels_[idx]].append(label)

    c_labels = [{'size': 0} for _ in range(7)]

    for i in range(len(clusters)):
        for item in clusters[i]:
            c_labels[i]['size'] += 1
            if item not in c_labels[i]:
                c_labels[i][item] = 0
            else:
                c_labels[i][item] += 1

    for i in range(len(c_labels)):
        print("************************************")
        for key in c_labels[i].keys():
            if key == 'size':
                continue

            c_labels[i][key] = c_labels[i][key] / c_labels[i]['size'] * 100
            # print(f"{key} : {c_labels[i][key] / c_labels[i]['size'] * 100}")
        del c_labels[i]['size']

    percents = c_labels

    # plt.scatter(x=data['p1'], y=data['p2'])
    # plt.show()

    # print(model.test)
    # print(len(model.test))


def trees():
    clf = DecisionTreeClassifier(random_state=0)
    with open('./all.pkl', 'rb') as inp:
        old: Kmeans = pkl.load(inp)

    print("started training")
    clf.fit(old.data.replace({None: 0}), old.order['company'])
    print("started validating")

    correct = 0
    wrong = 0
    size = len(old.test)

    t = old.test.iloc[0].replace({None: 0})
    ans = clf.predict(t.values.reshape(1, -1))
    print(ans)

    print(clf.decision_path(X=t.values.reshape(1, -1)))

    # print(clf.predict())
    for i in range(size):
        subject = old.test.iloc[i].replace({None: 0})
        predicted = clf.predict(subject.values.reshape(1, -1))
        label = old.testOrder.iloc[i]['company']

        if label == predicted[0]:
            correct += 1
        else:
            wrong += 1

    print(f"total samples: {size}")
    print(f"correct: {correct / size * 100}%, wrong: {wrong / size * 100}%")
    tree.plot_tree(clf)


# create_matrix()
# means()

# with open('./matrix.pkl', 'rb') as inp:
#     x = pkl.load(inp)
#     print(x)

trees()
