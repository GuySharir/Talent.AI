import argparse
import math
import sys
import os

import numpy as np
import pandas as pd
import copy
from datetime import datetime
import pickle as pkl
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

# sys.path.insert(0, os.path.abspath(os.path.abspath(os.getcwd())))

from program.DistanceFlow import run_distance_freq
from program.DistEnum import DistMethod
from program.DistanceFlow import inner_product_rep_dist, hamming_rep_dist, intersection_rep_dist, freq_rep_dist
from program.InstanceFreq import one_hot_rep, freq_rep, hamming_rep, loop_candidates_convert_to_freq_vec
from program.ReadData import set_path
import program.ReadData


def my_print(message):
    # print(inspect.stack()[1][3])
    print(message)


class Kmeans:
    def __init__(self,
                 n_clusters: int,
                 representation: DistMethod,
                 max_iter: int = 20):

        self.representation = representation

        if self.representation == DistMethod.intersection:
            self.distance_calc = intersection_rep_dist
            self.representation_conversion = one_hot_rep

        if self.representation == DistMethod.fix_length_freq:
            self.distance_calc = freq_rep_dist
            self.representation_conversion = freq_rep

        if self.representation == DistMethod.hamming_distance:
            self.distance_calc = hamming_rep_dist
            self.representation_conversion = hamming_rep

        if self.representation == DistMethod.inner_product:
            self.distance_calc = inner_product_rep_dist
            self.representation_conversion = one_hot_rep

        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.data: pd.DataFrame = None
        self.order: pd.DataFrame = None
        self.test: pd.DataFrame = None
        self.testOrder: pd.DataFrame = None
        self.load_data()
        self.centroids = []
        self.clusters = [[] for _ in range(n_clusters)]
        self.clusters_with_candidate_idx = [[] for _ in range(n_clusters)]
        self.clusters_distances = [[] for _ in range(n_clusters)]
        self.percents = None
        self.one_hot_vec = None

    def load_data(self) -> pd.DataFrame:

        print("started reading data")
        df = program.ReadData.read_local_json_employees()
        if self.representation == DistMethod.intersection:
            loop_candidates_convert_to_freq_vec(df, representation_option=DistMethod.fix_length_freq,
                                                representation_option_for_set=DistMethod.intersection,
                                                representation_option_for_nested=DistMethod.fix_length_freq)

        if self.representation == DistMethod.fix_length_freq:
            loop_candidates_convert_to_freq_vec(df, representation_option=DistMethod.fix_length_freq,
                                                representation_option_for_set=DistMethod.fix_length_freq,
                                                representation_option_for_nested=DistMethod.fix_length_freq)

        if self.representation == DistMethod.hamming_distance:
            loop_candidates_convert_to_freq_vec(df, representation_option=DistMethod.hamming_distance,
                                                representation_option_for_set=DistMethod.hamming_distance,
                                                representation_option_for_nested=DistMethod.hamming_distance)

        if self.representation == DistMethod.inner_product:
            loop_candidates_convert_to_freq_vec(df, representation_option=DistMethod.fix_length_freq,
                                                representation_option_for_set=DistMethod.inner_product,
                                                representation_option_for_nested=DistMethod.fix_length_freq)

        print(os.getcwd())
        raw_data = np.load('../dataTool/df_converted.npy', allow_pickle=True)

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
        combined = shuffle(combined, random_state=0)
        self.all = combined

        # combined = combined.sample(n=70, random_state=0)

        train, test = train_test_split(combined, test_size=0.2, random_state=0)

        self.order = train[['name', 'company']].copy()
        self.data = train.copy().drop(['name', "company"], axis=1).replace({np.nan: None})
        self.testOrder = test[['name', 'company']].copy()
        self.test = test.copy().drop(['name', "company"], axis=1).replace({np.nan: None})

        print(f"data len: {len(self.data)}, test len: {len(self.test)}")

    def initialize_centroids(self):
        for i in range(self.n_clusters):
            self.centroids.append(self.data.sample(n=1).values[0])

    def clear_clusters(self):
        for i in range(self.n_clusters):
            self.clusters[i].clear()
            self.clusters_with_candidate_idx[i].clear()

    def column_avrage(self, cluster):
        size = len(cluster[0])
        new_centroid = []

        for i in range(size):
            sum = 0
            reals = 0
            for entry in cluster:
                if entry[i] is not None:
                    reals += 1
                    sum += entry[i]

            if reals != 0:
                new_centroid.append(sum / reals)
            else:
                new_centroid.append(0)

        return new_centroid

    def calc_centroids(self):
        for i, cluster in enumerate(self.clusters):
            if len(cluster) != 0:
                self.centroids[i] = self.column_avrage(cluster)

    def find_closest_cluster(self, entry, first_loop: bool = False):
        distances = []
        for centroid in self.centroids:
            if self.representation == DistMethod.inner_product or self.representation == DistMethod.intersection:
                dist = self.distance_calc(entry, centroid, one_hot_inx_flag=first_loop)
                if self.one_hot_vec is None:
                    with open(set_path('dataTool/one_hot_index.json')) as f:
                        self.one_hot_vec = pd.read_json(f)
            else:
                dist = self.distance_calc(entry, centroid)
            distances.append(dist)

        best = np.argmin(distances)
        self.clusters_distances[best].append(distances[best])
        return best

    def add_to_cluster(self, cluster_idx, entry):
        self.clusters[cluster_idx].append(entry)

    def compare_centroids(self, index, old):

        for i in range(len(self.centroids[0])):
            if math.isnan(self.centroids[index][i]) and math.isnan(old[index][i]):
                continue

            if self.centroids[index][i] != old[index][i]:
                return False

        return True

    def show_clusters(self):

        print('\n clusters segmentation:')
        for i, cluster in enumerate(self.clusters):
            print(f"cluster: {i}, length: {len(cluster)}")

        # from sklearn.decomposition import TruncatedSVD
        # svd = TruncatedSVD(n_components=2, n_iter=7)

        pca = PCA(n_components=2)
        tmp = self.data.replace({None: 0})

        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(tmp)

        # Normalizing the Data
        normalized_df = normalize(scaled_df)

        # Converting the numpy array into a pandas DataFrame
        normalized_df = pd.DataFrame(normalized_df)

        x_principal = pca.fit_transform(normalized_df)
        x_principal = pd.DataFrame(x_principal)
        x_principal.columns = ['x', 'y']

        # tmp = []
        #
        # for i in range(len(x_principal)):
        #     for number, cluster in enumerate(self.clusters_with_candidate_idx):
        #         if i in cluster:
        #             tmp.append(number)

        for i in range(self.n_clusters):
            tmp = x_principal.iloc[self.clusters_with_candidate_idx[i]]
            plt.scatter(tmp['x'], tmp['y'])

        plt.show()

    def fit(self):
        self.initialize_centroids()
        size = len(self.data)
        first_loop = True

        for iteration in range(self.max_iter):
            print(f"starting iteration {iteration}")
            print([len(x) for x in self.clusters])
            # print(self.clusters_distances)
            self.clear_clusters()
            self.clusters_distances = [[] for _ in range(self.n_clusters)]

            for idx in range(size):
                entry = list(self.data.iloc[idx])
                cluster_idx = self.find_closest_cluster(entry, first_loop)
                first_loop = False
                self.add_to_cluster(cluster_idx, entry)
                self.clusters_with_candidate_idx[cluster_idx].append(idx)

            # self.show_clusters()

            old_centroids = copy.deepcopy(self.centroids)
            self.calc_centroids()

            stop = True
            for i in range(self.n_clusters):
                if not self.compare_centroids(i, old_centroids):
                    stop = False
                    break

            if stop:
                print("exited since no centroides were changed")
                break

            self.calc_percents(show=False)

    def predict(self, entry: dict):
        converted = self.representation_conversion(entry)
        return self.find_closest_cluster(converted, False)

    def company_order(self, candidates: list, job_offer: dict, gender: bool = False, age: bool = False):
        scores = []
        job_converted = self.representation_conversion(job_offer)
        for i, candidate in enumerate(candidates):
            converted = self.representation_conversion(vars(candidate))
            scores.append([i, self.distance_calc(converted, job_converted, gender=gender, birth_year=age)])

        scores.sort(key=lambda score: score[1])
        return scores

    def calc_percents(self, show=True):
        percents = {}
        clusters = [[] for _ in range(self.n_clusters)]

        for i, cluster in enumerate(self.clusters_with_candidate_idx):
            for j, can in enumerate(cluster):
                clusters[i].append(self.order.iloc[j]['company'])

        for i, cluster in enumerate(clusters):
            options = set(cluster)
            sums = {}
            size = len(cluster)
            for option in options:
                sums[option] = (cluster.count(option) / size * 100, cluster.count(option))

            percents[i] = sums

        self.percents = percents

        if show:
            self.print_cluster_company_percent()

    def print_cluster_company_percent(self):
        for k in self.percents:
            print(f"\n********         cluster {k + 1}:         ********")
            for row in self.percents[k]:
                print(f"{row}: {self.percents[k][row][0]}, total: {self.percents[k][row][1]} ")

    def check_test_group(self):
        size = len(self.test)

        precision = [
            {
                "correct": 0,
                "wrong": 0
            },
            {
                "correct": 0,
                "wrong": 0
            },
            {
                "correct": 0,
                "wrong": 0
            },
            {
                "correct": 0,
                "wrong": 0
            },
            {
                "correct": 0,
                "wrong": 0
            }
        ]

        correct = 0
        wrong = 0

        for idx in range(size):
            entry = list(self.test.iloc[idx])
            label = self.testOrder.iloc[idx]['company']

            cluster = self.find_closest_cluster(entry)
            # self.calc_precision(precision, label, cluster)
            ordered = {k: v for k, v in sorted(self.percents[cluster].items(), reverse=True, key=lambda item: item[1])}
            ordered = ordered.keys()

            if list(ordered)[0] == label:
                correct += 1
            else:
                wrong += 1

        print(f"correct: {correct / size}, wrong: {wrong / size}")

    def calc_precision(self, precision, label, cluster_idx):
        ordered = {k: v for k, v in sorted(self.percents[cluster_idx].items(), reverse=True, key=lambda item: item[1])}
        ordered = ordered.keys()

        success = False
        for i, item in enumerate(ordered):
            if i == 4:
                if success:
                    precision[i]['correct'] += 1
                else:
                    precision[i]['wrong'] += 1
                break

            if item == label:
                precision[i]['correct'] += 1
                success = True
            else:
                precision[i]['wrong'] += 1


def create_matrix():
    # with open('./freqRepAll.pkl', 'rb') as inp:
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000000)
    raw_data = np.load("all.npy", allow_pickle=True)
    data = []
    order = []
    counter = 0
    for row in raw_data:
        converted = list(row.values())
        data.append(converted[0][1])
        order.append((list(row.keys())[0], converted[0][0]))

    data = pd.DataFrame(data)
    order = pd.DataFrame(order)

    order.rename(columns={0: "name", 1: "company"}, inplace=True)

    combined: pd.DataFrame = pd.concat([data, order], axis=1)
    combined = shuffle(combined)

    order = combined[['name', 'company']].copy()
    data = combined.copy().drop(['name', "company"], axis=1)

    # np.save('data450.npy', data)
    # np.save('order450.npy', order)

    size = len(data)
    distances = np.zeros((size, size))

    start = 0

    data = data.replace({np.nan: None})

    for i in range(size):
        if i == 0:
            start = datetime.now()
        if i == 1:
            now = datetime.now()
            diff = now - start
            print(f"total time to calculate will be: {diff.total_seconds() / 60 * size} minutes")

        print(f"now calculating the {i} row out of {size}")

        for j in range(i, size):
            distances[i][j] = distances[j][i] = run_distance_freq(list(data.iloc[i]), list(data.iloc[j]),
                                                                  representation_option=DistMethod.fix_length_freq,
                                                                  representation_option_set=DistMethod.fix_length_freq)

    np.save("distances.npy", distances)
    np.save("order.npy", order)

    with open('distances.pkl', 'wb') as f:
        pkl.dump(distances, f)

    with open('order.pkl', 'wb') as f:
        pkl.dump(order, f)


def find_inner_correlation():
    with open('6cluster.pkl', 'rb') as file:
        x: Kmeans = pkl.load(file)
        x.show_clusters()

    original = program.ReadData.read_local_json_employees()

    for i, cluster in enumerate(x.clusters_with_candidate_idx):
        roles = {'name': {}, 'role': {}}
        print(f"***************** displaying cluster {i} ********************")
        for idx in cluster:
            cand = original[original['full_name'] == x.order.iloc[idx]['name']]
            positions = cand['experience'].values

            for pos in positions[0]:
                if pos['current_job'] == True:
                    if pos['title_name'] not in roles['name']:
                        roles['name'][pos['title_name']] = 1
                    else:
                        roles['name'][pos['title_name']] += 1

                    if pos['title_role'] not in roles['role']:
                        roles['role'][pos['title_role']] = 1
                    else:
                        roles['role'][pos['title_role']] += 1

        for key in {k: v for k, v in sorted(roles["name"].items(), key=lambda item: item[1])}:
            print(f"key: {key}, amount: {roles['name'][key]}")

        print(f"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        for key in {k: v for k, v in sorted(roles["role"].items(), key=lambda item: item[1], reverse=True)}:
            print(f"key: {key}, amount: {roles['role'][key]}")

        print(f"\n\n\n")


def calc_elbow():
    pass
    wcss = []
    for i in range(2, 18):
        model = Kmeans(i, representation=DistMethod.fix_length_freq)
        model.fit()
        total = 0
        for cluster in model.clusters_distances:
            total += sum([number ** 2 for number in cluster])
        wcss.append(total)
        print(f"******  wcss: {wcss}")

    print(wcss)
    plt.plot(range(2, 18), wcss)
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()


if __name__ == "__main__":
    model = Kmeans(7, representation=DistMethod.fix_length_freq)
    # model.fit()
    # #
    with open('five_my.pkl', 'wb') as f:
        pkl.dump(model, f)
    #
    # model.check_test_group()

    # calc_elbow()

    # with open('./all.pkl', 'rb') as file:
    #     model: Kmeans = pkl.load(file)

    #     for key in model.percents:
    #         print(model.percents[key])
    #
    # pd.set_option('display.max_rows', None, 'display.max_columns', None)
    # print(model.data.iloc[0])
    # create_matrix()
