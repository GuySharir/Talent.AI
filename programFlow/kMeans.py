import argparse
import sys
import os
import requests

import numpy as np
import pandas as pd
import copy
import pickle

sys.path.insert(0, os.path.abspath(os.path.abspath(os.getcwd())))
# from programFlow.DistFunctions import prepare_data_for_dist_calc_between_freq_vectors
from DistFunctions import prepare_data_for_dist_calc_between_freq_vectors
from InstanceFreq import convert_instance_to_freq_vec
from sklearn.utils import shuffle


def my_print(message):
    # print(inspect.stack()[1][3])
    print(message)


class Kmeans:

    def __init__(self, dataPath: str, n_clusters: int, max_iter: int = 20, random_state: int = None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.data: pd.DataFrame = None
        self.order: pd.DataFrame = None
        self.load_data(dataPath)
        self.centroids = []
        self.clusters = [[] for _ in range(n_clusters)]
        self.clusters_by_index = [[] for _ in range(n_clusters)]
        self.distance_calc = prepare_data_for_dist_calc_between_freq_vectors
        self.percents = None

        # print(self.data)

    def load_data(self, dataPath: str) -> pd.DataFrame:
        raw_data = np.load(dataPath, allow_pickle=True)
        data = []
        order = []
        for row in raw_data:
            converted = list(row.values())
            data.append(converted[0][1])
            order.append((list(row.keys())[0], converted[0][0]))

        data = pd.DataFrame(data)
        order = pd.DataFrame(order)

        order.rename(columns={0: "name", 1: "company"}, inplace=True)

        combined: pd.DataFrame = pd.concat([data, order], axis=1)
        combined = shuffle(combined)

        # combined = combined.sample(n=100)

        self.order = combined[['name', 'company']].copy()
        self.data = combined.copy().drop(['name', "company"], axis=1)

    def initialize_centroids(self):
        size = self.data.shape[1]
        for i in range(self.n_clusters):
            # print(self.data.sample(n=1).values[0])
            self.centroids.append(self.data.sample(n=1).values[0])

    def clear_clusters(self):
        for i in range(self.n_clusters):
            self.clusters[i].clear()
            self.clusters_by_index[i].clear()

    def calc_centroids(self):
        i = 0
        for cluster in self.clusters:
            if len(cluster) != 0:
                tmp = np.average(cluster, axis=0)
                self.centroids[i] = tmp
            i += 1

    def find_closest_cluster(self, entry):
        distances = []
        for centroid in self.centroids:
            distances.append(self.distance_calc(entry, centroid))

        return np.argmin(distances)

    def add_to_cluster(self, cluster_idx, entry):
        self.clusters[cluster_idx].append(entry)

    def print_list(self, data):
        for row in data:
            print(row)

    def cluster_percents(self):

        percents = {}

        idx = 0
        for cluster in self.clusters_by_index:
            tmp = []
            for i in cluster:
                tmp.append(self.order.iloc[i]['name'])
            percents[idx] = tmp

    def fit(self):
        self.initialize_centroids()
        size = len(self.data)

        for iteration in range(self.max_iter):
            print(f"starting iteration {iteration}")
            self.clear_clusters()

            for idx in range(size):
                entry = list(self.data.iloc[idx])

                cluster_idx = self.find_closest_cluster(entry)
                self.add_to_cluster(cluster_idx, entry)
                self.clusters_by_index[cluster_idx].append(idx)

            old_centroids = copy.deepcopy(self.centroids)
            self.calc_centroids()

            stop = True
            for i in range(self.n_clusters):
                if np.all(old_centroids[i] != self.centroids[i]):
                    stop = False

            if stop:
                break

    def predict(self, entry):
        return self.find_closest_cluster(entry)

    def calc_percents(self, show=True):
        percents = {}
        clusters = [[] for _ in range(self.n_clusters)]

        for i, cluster in enumerate(self.clusters_by_index):
            for j, can in enumerate(cluster):
                clusters[i].append(self.order.iloc[j]['company'])

        for i, cluster in enumerate(clusters):
            options = set(cluster)
            sums = {}
            size = len(cluster)
            for option in options:
                sums[option] = cluster.count(option) / size * 100

            percents[i] = sums

        self.percents = percents

        if show:
            self.print_cluster_company_percent()

    def print_cluster_company_percent(self):
        for k in self.percents:
            print(f"\n********         cluster {k + 1}:         ********")
            for row in self.percents[k]:
                print(f"{row}: {self.percents[k][row]}")


# def get_user_by

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.abspath(os.getcwd())))
    # payload = {'guy sharir': 1, "opal peltamzn": "loserit"}
    # r = requests.post('http://127.0.0.1:3000/api/candidate/forAlgo', data=payload)
    # print(r.json)
    with open('../model.pkl', 'rb') as inp:
        model = pickle.load(inp)
        model.print_cluster_company_percent()

        # parser = argparse.ArgumentParser(description='Process some integers.')
        # parser.add_argument('--cand', type=str, nargs='*')
        # parser.add_argument('--func', type=str, nargs='*')
        # parser.add_argument('--job', type=str, default='')
        # args = parser.parse_args()
        #
        # func = args.func
        #
        # if func[0] == "candidate":
        #     users = args.cand
        #     users = [user.replace('_', ' ') for user in users]
        #     payload = {"candidates": users}
        #     req = requests.post('http://127.0.0.1:3000/api/candidate/forAlgo', data=payload)
        #     candidate = req.json()[0]
        #     candidate.pop('_id')
        #
        #     candidate = convert_instance_to_freq_vec(candidate)
        #     candidate = list(candidate.values())[0][1]
        #     percents = model.percents
        #     prediction = model.predict(candidate)
        #     #
        #     print(f"$${percents[prediction]}", flush=True)

sys.exit(0)
# elif func[0] == "company":
#     users_ = args.cand
#     id = args.job
#     pass
