import math
import os

import numpy as np
import pandas as pd
import copy
from datetime import datetime
import pickle as pkl
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize, StandardScaler, MinMaxScaler
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
import json


def my_print(message):
    # print(inspect.stack()[1][3])
    print(message)


class Kmeans:
    def __init__(self, n_clusters: int, representation: DistMethod, max_iter: int = 20):

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
        self.clusters_inner_centroids = [{} for _ in range(n_clusters)]
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

        raw_data = np.load('./dataTool/df_converted.npy', allow_pickle=True)

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

        combined = combined.sample(n=60, random_state=0)

        train, test = train_test_split(combined, test_size=0.2, random_state=0)

        self.order = train[['name', 'company']].copy()
        self.data = train.copy().drop(['name', "company"], axis=1).replace({np.nan: None})
        self.testOrder = test[['name', 'company']].copy()
        self.test = test.copy().drop(['name', "company"], axis=1).replace({np.nan: None})

        print(f"data len: {len(self.data)}, test len: {len(self.test)}")

    def initialize_centroids(self):
        """
        initiate centroids randomlly from within the data
        :return:
        """
        centroids = self.data.sample(n=self.n_clusters, random_state=0)
        for i in range(self.n_clusters):
            self.centroids.append(centroids.iloc[i].values)

    def clear_clusters(self):
        """
        clear clusters in order to re calculate the clusters
        :return:
        """
        for i in range(self.n_clusters):
            self.clusters[i].clear()
            self.clusters_with_candidate_idx[i].clear()

    def frequency_representaion_centroid_calc(self, cluster):
        size = len(cluster[0])
        new_centroid = []

        for i in range(size):
            total_frequency = 0
            not_none = 0
            for entry in cluster:
                if entry[i] is not None:
                    not_none += 1
                    total_frequency += entry[i]

            if not_none != 0:
                new_centroid.append(total_frequency / not_none)
            else:
                new_centroid.append(0)

        return new_centroid

    def onehot_representaion_centroid_calc(self, cluster):
        vector_length = len(cluster[0])
        group_size = len(cluster)
        new_centroid = []
        with open("dataTool/one_hot_index.json") as f:
            indexes = json.load(f)

        for i in range(vector_length):
            if i in indexes:
                total = 0
                for entry in cluster:
                    total += entry[i]

                new_centroid.append(round(total / group_size))

            else:
                # need to calc by regular sum while ignoring none
                total_frequency = 0
                not_none = 0
                for entry in cluster:
                    if entry[i] is not None:
                        not_none += 1
                        total_frequency += entry[i]

                if not_none != 0:
                    new_centroid.append(total_frequency / not_none)
                else:
                    new_centroid.append(0)

        return new_centroid

    def hamming_representaion_centroid_calc(self, cluster):

        vector_length = len(cluster[0])
        new_centroid = []

        # we shuffle the entrys in the cluster so that selected val in case of tie will be random
        cluster = shuffle(cluster)

        for i in range(vector_length):
            dp = {}
            max_freq = ("", 0)
            for entry in cluster:
                val = entry[i]
                if val not in dp:
                    dp[val] = 1
                else:
                    dp[val] += 1

                amount = dp[val]
                if amount > max_freq[1]:
                    max_freq = (val, amount)

            new_centroid.append(max_freq[0])

        return new_centroid

    def calc_centroids_by_representation(self, cluster):
        """
        function to calculate the new centroid based on self.representation\n
        if rep is freq - then each column gets the avg frequency\n
        if rep is inner product or intersection - then each column gets the majorty voting\n
        if rep is hamming - each column gets the most frequent value within the cluster\n
        :param cluster: the group of vectors we need to use inorder to calcuate the new centroid
        :return: new_centroid
        """

        if self.representation == DistMethod.intersection or self.representation == DistMethod.inner_product:
            new_centroid = self.onehot_representaion_centroid_calc(cluster)

        if self.representation == DistMethod.hamming_distance:
            new_centroid = self.hamming_representaion_centroid_calc(cluster)

        if self.representation == DistMethod.fix_length_freq:
            new_centroid = self.frequency_representaion_centroid_calc(cluster)

        return new_centroid

    def calc_centroids(self):
        """
        calculate the new representative for the cluster centroid, calculation depends on the representation option
        chosen when model is created
        """
        for i, cluster in enumerate(self.clusters):
            if len(cluster) != 0:
                self.centroids[i] = self.calc_centroids_by_representation(cluster)

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
            if not isinstance(self.centroids[index][i], str):
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
            self.clear_clusters()
            self.clusters_distances = [[] for _ in range(self.n_clusters)]

            for idx in range(size):
                entry = list(self.data.iloc[idx])
                cluster_idx = self.find_closest_cluster(entry, first_loop)
                first_loop = False
                self.add_to_cluster(cluster_idx, entry)
                self.clusters_with_candidate_idx[cluster_idx].append(idx)

            old_centroids = copy.deepcopy(self.centroids)
            self.calc_centroids()

            stop = True
            for i in range(self.n_clusters):
                if not self.compare_centroids(i, old_centroids):
                    stop = False
                    break

            if stop:
                print("exited since no centroids were changed")
                break

            self.calc_percents(show=False)

    def calc_inner_centroids(self):

        clusters = self.calc_inner_segmentation()

        for i, cluster in enumerate(clusters):
            for key in cluster:
                tmp = []
                for idx in cluster[key]:
                    tmp.append(self.data.iloc[idx])

                centroid = self.calc_centroids_by_representation(tmp)
                self.clusters_inner_centroids[i][key] = centroid

    def calc_inner_segmentation(self):
        clusters = [{} for _ in range(self.n_clusters)]

        for i, cluster in enumerate(self.clusters_with_candidate_idx):
            for can in cluster:
                label = self.order.iloc[can]['company']
                if label not in clusters[i]:
                    clusters[i][label] = [can]
                else:
                    clusters[i][label].append(can)

        return clusters
        # for x in clusters:
        #     print(x)

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
                clusters[i].append(self.order.iloc[can]['company'])

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
        """
        utility function, prints the calculated percents to stdout
        :return: none
        """
        for k in self.percents:
            print(f"\n********         cluster {k + 1}:         ********")
            for row in self.percents[k]:
                print(f"{row}: {self.percents[k][row][0]}, total: {self.percents[k][row][1]} ")

    def check_test_group(self, threshold=3):
        """
        :param threshold: what is the level the from which we check if  there was a hit in all levels to threshold
        :return: precision object, prints precision to stdout
        """
        size = len(self.test)

        single_precision = {
            "correct": 0,
            "wrong": 0
        }
        precision = [dict(single_precision) for i in range(threshold + 1)]

        for idx in range(size):
            entry = list(self.test.iloc[idx])
            label = self.testOrder.iloc[idx]['company']

            cluster = self.find_closest_cluster(entry)
            self.calc_precision(precision, label, cluster)

        for i in range(4):
            if i == 3:
                print("one of the three highest:")
            else:
                print(f"matches the {i + 1} highest option:")
            c = precision[i]['correct']
            w = precision[i]['wrong']
            print(f"correct: {c / (c + w) * 100}5, wrong: {w / (c + w) * 100}\n")
            print(precision[i])

        return precision

    def calc_precision(self, precision, label, cluster_idx):
        ordered = {k: v for k, v in sorted(self.percents[cluster_idx].items(), reverse=True, key=lambda item: item[1])}
        ordered = ordered.keys()
        print(ordered)
        success = False
        for i, item in enumerate(ordered):
            if i == 3:
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

    def predict_v2(self, entry: dict):
        converted = self.representation_conversion(entry)
        cluster_idx = self.find_closest_cluster(converted, False)
        distances = []
        centroids = self.clusters_inner_centroids[cluster_idx]

        for key in centroids:
            distances.append((key, self.distance_calc(converted, centroids[key])))

        return distances


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


# def calc_clustering_quality(path_a, path_b, path_c, n_clusters):
#     with open(path_a, 'rb') as file:
#         freq: Kmeans = pkl.load(file)
#
#     with open(path_b, 'rb') as file:
#         hamming: Kmeans = pkl.load(file)
#
#     with open(path_c, 'rb') as file:
#         intersection: Kmeans = pkl.load(file)
#
#     normalized = [[] for _ in range(n_clusters)]
#
#     _min = None
#     _max = None
#
#     for version in [hamming.clusters_distances, intersection.clusters_distances, freq.clusters_distances]:
#         for cluster in version:
#             if _min is None:
#                 _min = min(cluster)
#                 _max = max(cluster)
#             else:
#                 _min = min(cluster) if min(cluster) < _min else _min
#                 _max = max(cluster) if max(cluster) > _max else _max
#
#     print(_min)
#     print(_max)
#
#     normalized = []
#
#     for version in [hamming.clusters_distances, intersection.clusters_distances, freq.clusters_distances]:
#         tmp = [[] for _ in range(n_clusters)]
#         for i, cluster in enumerate(version):
#             for val in cluster:
#                 norm = (val - _min) / (_max - _min)
#                 tmp[i].append(norm)
#
#         normalized.append(tmp)
#
#     total = 0
#
#     for version in normalized:
#         tmp = []
#         for cluster in version:
#             tmp.append(sum([number ** 2 for number in cluster]))
#
#         print(tmp)
#         print(sum(tmp))
#
#     # X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
#
#     # for cluster in model.clusters_distances:
#     #     total += sum([number ** 2 for number in cluster])
#
#     return total / 7

def calc_clustering_quality(path):
    with open(path, 'rb') as file:
        model: Kmeans = pkl.load(file)

    _min = None
    _max = None

    for cluster in model.clusters_distances:
        if _min is None:
            _min = min(cluster)
            _max = max(cluster)
        else:
            _min = min(cluster) if min(cluster) < _min else _min
            _max = max(cluster) if max(cluster) > _max else _max

    print(_min)
    print(_max)

    normalized = []

    for cluster in model.clusters_distances:
        tmp = []
        for val in cluster:
            norm = (val - _min) / (_max - _min)
            tmp.append(norm ** 2)

        normalized.append(tmp)

    sums = [sum(cluster) for cluster in normalized]

    print(f"sums: {sums}")
    print(f"total sum: {sum(sums)}")
    print(f"mean: {sum(sums) / model.n_clusters}")

    # X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))

    # for cluster in model.clusters_distances:
    #     total += sum([number ** 2 for number in cluster])


if __name__ == "__main__":
    # model = Kmeans(8, representation=DistMethod.fix_length_freq)
    # model.fit()
    # with open('clustering/precisionModels/demo.pkl', 'wb') as f:
    #     pkl.dump(model, f)

    # model.check_test_group()
    # calc_elbow()

    # a = calc_clustering_quality('clustering/precisionModels/frequency_based.pkl',
    #                             'clustering/precisionModels/hamming_based.pkl',
    #                             'clustering/precisionModels/intersection_based.pkl', 7)

    # calc_clustering_quality('clustering/precisionModels/frequency_based.pkl')
    # calc_clustering_quality('clustering/precisionModels/intersection_based.pkl')
    # calc_clustering_quality('clustering/precisionModels/hamming_based.pkl')

    # print(a)
    # print(b)
    # print(c)

    with open('clustering/precisionModels/demo.pkl', 'rb') as file:
        model: Kmeans = pkl.load(file)
        # model.calc_percents()
        # model.calc_inner_segmentation()
