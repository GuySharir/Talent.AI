import itertools
import math
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from collections import defaultdict
import sklearn.cluster
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, normalize, StandardScaler
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import matplotlib.cm as cm
from termcolor import colored


# def my_kmeans(n_clusters):
#     data = load_data('five.npy')
#     order = load_data('fiveOrderCompany.npy')
#
#     order.rename(columns={0: "name", 1: "company"}, inplace=True)
#
#     # data = scale_data(data, "minmax")
#     data = scale_data(data, "standard")
#     data = normalize_data(data)
#
#     data = reduce_dimension(data)
#
#     # concat both actual labels and feature dataFrame so shuffle would be performed equally
#     data = pd.concat([data, order], axis=1)
#     data = shuffle(data, random_state=0)
#
#     # train, test = split_data_train_test(data)
#
#     train = data
#
#     train_x = train.copy().drop(['name', 'company'], axis=1)
#     train_y = train[['name', 'company']].copy()
#
#     # test_x = test.copy().drop(['name', 'company'], axis=1)
#     # test_y = test[['name', 'company']].copy()
#
#     kmeans = KMeans(n_clusters=n_clusters, random_state=0)
#     kmeans.fit(train_x)
#
#     labels = kmeans.labels_
#     centers = kmeans.cluster_centers_
#
#     find_real_centers(train_y, train_x, labels, centers, n_clusters)
#
#     # for key in dataframes:
#     #     print('\n')
#     #     print(dataframes[key])
#
#     # percents, names = calc_clusters_company_percent(labels, n_clusters, train_y, show=True)
#     # predictions = kmeans.predict(test_x)
#     # calc_precision(predictions, test_y, percents, True)


class MyKmeans:
    def prepare_data(self):
        self.order.rename(columns={0: "name", 1: "company"}, inplace=True)

        self.data = self.scale_data("standard")
        self.data = self.normalize_data()
        self.data = self.reduce_dimension()

        # concat both actual labels and feature dataFrame so shuffle would be performed equally
        self.data = pd.concat([self.data, self.order], axis=1)
        self.data = shuffle(self.data, random_state=0)

    def split_data(self):
        train_x = self.data.copy().drop(['name', 'company'], axis=1)
        train_y = self.data[['name', 'company']].copy()

        return train_x, train_y

    def __init__(self, n_clusters: int, data_path: str, order_path: str):
        self.data = self.load_data(data_path)
        self.order = self.load_data(order_path)
        self.prepare_data()
        self.n_clusters = n_clusters

        self.data_x, self.data_y = self.split_data()

        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(self.data_x)

        self.labels = kmeans.labels_
        self.centers = kmeans.cluster_centers_
        self.real_centers = self.find_real_centers()
        self.percents, self.names = self.calc_clusters_company_percent()

        print(self.percents)

    def reduce_dimension(self) -> pd.DataFrame:
        pca = PCA(n_components=2)
        x_principal = pca.fit_transform(self.data)
        x_principal = pd.DataFrame(x_principal)
        x_principal.columns = ['p1', 'p2']
        return x_principal

    def load_data(self, path) -> pd.DataFrame:
        raw_df = np.load(path)
        raw_df = pd.DataFrame(raw_df)
        return raw_df

    def normalize_data(self) -> pd.DataFrame:
        return

    def scale_data(self, scaler_type: str) -> pd.DataFrame:
        if scaler_type == "standard":
            scaler = StandardScaler()
            return scaler.fit_transform(self.data)

        if scaler_type == "minmax":
            mms = MinMaxScaler()
            return mms.fit_transform(self.data)

        print(f"option: {scaler_type} is not recognized. returning original df")
        return self.data

    def split_data_train_test(self, train_percent: float = 0.8):
        index = math.floor(len(self.data) * train_percent)
        train = self.data.iloc[0:index]
        test = self.data.iloc[index + 1:-1]

        return train, test

    def print_cluster_company_percent(self, clusters):
        for cluster in clusters:
            print(f"\n********** cluster {cluster} **********")
            for val in clusters[cluster]:
                print(f"{val[0]} - {val[1]}")

            print(f"\n############## done cluster {cluster} ##############\n")

            # x = list([val[0] for val in clusters[cluster]])
            # y = list([val[1] for val in clusters[cluster]])
            # fig = plt.figure(figsize=(10, 5))
            # plt.bar(x, y, color='blue',
            #         width=0.4)
            #
            # plt.xlabel("Hit number inside cluster")
            # plt.ylabel("Percent os candidates")
            # plt.yticks(np.arange(0, 60, 5))
            # plt.show()

    def calc_clusters_company_percent(self, show=False):
        clusters = [[] for _ in range(self.n_clusters)]
        for i, label in enumerate(self.labels):
            clusters[label].append(self.data_y.iloc[i]['company'])

        names = {}
        percents = {}

        for i, cluster in enumerate(clusters):
            options = set(cluster)
            sums = {}
            size = len(cluster)
            for option in options:
                sums[option] = cluster.count(option) / size * 100

            # sums.sort(key=lambda x: x[1], reverse=True)
            # sums = {k: v for k, v in sorted(sums.items(), key=lambda item: item[1])}
            # names[i] = sums[0][0]
            percents[i] = sums
            names = []

        if show:
            self.print_cluster_company_percent(percents, names)

        return percents, names

    def calc_precision(self, predictions, test_y: pd.DataFrame, percents, show=False):
        hits = defaultdict(int)
        size = len(test_y)

        hits[0] = 0

        for i, pred in enumerate(predictions):
            percent = percents[pred]

            found = False
            for j, val in enumerate(percent):
                if val[0] == test_y.iloc[i]['company']:
                    hits[pred + 1] += 1
                    found = True

            if not found:
                hits[-1] += 1

        hits = {k: v for k, v in sorted(hits.items(), reverse=True, key=lambda item: item[1])}

        for key in hits:
            print(f"{hits[key] / size * 100}% matched the {key} option")

        # x = list(hits.keys())
        # y = list(hits.values())
        # fig = plt.figure(figsize=(10, 5))
        # plt.bar(x, y, color='maroon',
        #         width=0.4)
        #
        # plt.xlabel("Hit number inside cluster")
        # plt.ylabel("Percent os candidates")
        # plt.show()

        return hits

    def find_real_centers(self):
        groups = pd.DataFrame(columns=['cluster', 'name', 'p1', 'p2'])

        for i, label in enumerate(self.labels):
            groups = groups.append(
                {'cluster': label, 'name': self.data_y.iloc[i]['name'], 'p1': self.data_x.iloc[i]['p1'],
                 'p2': self.data_x.iloc[i]['p2']},
                ignore_index=True)

        dataframes = {}

        for i in range(self.n_clusters):
            dataframes[i] = groups[groups['cluster'] == i]

        real_centers = pd.DataFrame(columns=['name', 'p1', 'p2', 'center_1', 'center_2'])

        for i in range(self.n_clusters):
            closest = ('', 1000000, 0, 0)
            center = self.centers[i]

            for j in range(len(dataframes[i])):
                row = dataframes[i].iloc[j]
                first = (row['p1'] - center[0]) ** 2
                second = (row['p2'] - center[1]) ** 2
                dist = math.sqrt(first + second)

                if dist <= closest[1]:
                    closest = (row['name'], dist, row['p1'], row['p2'], center[0], center[1])

            real_centers = real_centers.append(
                {'name': closest[0], 'p1': closest[2], 'cluster': i,
                 'p2': closest[3], 'center_1': closest[4], 'center_2': closest[5]}, ignore_index=True)

        return real_centers.copy().drop(['p1', 'p2', 'center_1', 'center_2'], axis=1)

    def get_cluster_for_candidate(self):
        pass


if __name__ == '__main__':
    x = MyKmeans(5, 'five.npy', 'fiveOrderCompany.npy')
