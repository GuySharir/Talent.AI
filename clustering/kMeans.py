import math
import random

import numpy as np
import pandas as pd
import copy
from datetime import datetime
import pickle as pkl
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize, StandardScaler, Normalizer
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from program.DistanceFlow import run_distance_freq
from program.DistEnum import DistMethod
from program.DistanceFlow import inner_product_rep_dist, hamming_rep_dist, intersection_rep_dist, freq_rep_dist
from program.InstanceFreq import one_hot_rep, freq_rep, hamming_rep, loop_candidates_convert_to_freq_vec
from program.ReadData import set_path
import program.ReadData
import json


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

    def set_hyper_params(self, t1: int = 3, t2: int = 10, beta: float = 0.05, gama: float = 0.01):
        self.t1 = t1
        self.t2 = t2
        self.beta = beta
        self.gama = gama

    def load_data(self) -> pd.DataFrame:
        """
        Load the data from the json files in order to train the model.
        """
        df = program.ReadData.read_local_json_employees()

        df = df.sample(n=250, random_state=1)

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
        raw_data = np.load('../dataTool/df_genetic_alg.npy', allow_pickle=True)

        # data for genetic algorithm
        # raw_data = np.load('../dataTool/df_genetic_alg.npy', allow_pickle=True)

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

        self.order = combined[['name', 'company']].copy()
        self.data = combined.copy().drop(
            ['name', "company"], axis=1).replace({np.nan: None})

    def initialize_centroids(self):
        """
        initiate centroids randomly from within the data
        """
        centroids = self.data.sample(n=self.n_clusters, random_state=0)
        for i in range(self.n_clusters):
            self.centroids.append(centroids.iloc[i].values)

    def clear_clusters(self):
        """
        clear clusters in order to re calculate the clusters
        """
        for i in range(self.n_clusters):
            self.clusters[i].clear()
            self.clusters_with_candidate_idx[i].clear()

    def frequency_representation_centroid_calc(self, cluster):
        """
        Calc centroids for a given cluster based on the frequency representation
        """
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

    def onehot_representation_centroid_calc(self, cluster):
        """
        Calc centroids for a given cluster based on the onehot representation
        """
        vector_length = len(cluster[0])
        group_size = len(cluster)
        new_centroid = []
        with open("../dataTool/one_hot_index.json") as f:
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

    def hamming_representation_centroid_calc(self, cluster):
        """
        Calc centroids for a given cluster based on the hamming representation
        """

        vector_length = len(cluster[0])
        new_centroid = []

        # we shuffle the entries in the cluster so that selected val in case of tie will be random
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
            new_centroid = self.onehot_representation_centroid_calc(cluster)

        if self.representation == DistMethod.hamming_distance:
            new_centroid = self.hamming_representation_centroid_calc(cluster)

        if self.representation == DistMethod.fix_length_freq:
            new_centroid = self.frequency_representation_centroid_calc(cluster)

        return new_centroid

    def calc_centroids(self):
        """
        calculate the new representative for the cluster centroid, calculation depends on the representation option
        chosen when model is created
        """
        for i, cluster in enumerate(self.clusters):
            if len(cluster) != 0:
                self.centroids[i] = self.calc_centroids_by_representation(
                    cluster)

    def calc_inner_centroids(self):
        """
        create a representative for each company at each cluster
        """
        clusters = self.calc_inner_segmentation()

        for i, cluster in enumerate(clusters):
            for key in cluster:
                tmp = []
                for idx in cluster[key]:
                    tmp.append(self.data.iloc[idx])

                centroid = self.calc_centroids_by_representation(tmp)
                self.clusters_inner_centroids[i][key] = centroid

    def find_closest_cluster(self, entry, first_loop: bool = False,validation=False):
        """
        Function that finds the closest cluster 
        """
        distances = []
        for centroid in self.centroids:
            if self.representation == DistMethod.inner_product or self.representation == DistMethod.intersection:
                dist = self.distance_calc(
                    entry, centroid, one_hot_inx_flag=first_loop)
                if self.one_hot_vec is None:
                    with open(set_path('dataTool/one_hot_index.json')) as f:
                        self.one_hot_vec = pd.read_json(f)
            elif self.representation == DistMethod.fix_length_freq:
                dist = self.distance_calc(entry, centroid, t1=self.t1, t2=self.t2, beta=self.beta, gama=self.gama)
            else:
                dist = self.distance_calc(entry, centroid)
            distances.append(dist)

        best = np.argmin(distances)
        if not validation:
            self.clusters_distances[best].append(distances[best])
        return best

    def add_to_cluster(self, cluster_idx, entry):
        self.clusters[cluster_idx].append(entry)

    def compare_centroids(self, index, old):
        """
        check if centroids were changed in order to decide whether we should start another iteration
        """
        for i in range(len(self.centroids[0])):
            if not isinstance(self.centroids[index][i], str):
                pass
                # print(index,i)
                # if math.isnan(self.centroids[index][i]) and math.isnan(old[index][i]):
                #     continue

            if self.centroids[index][i] != old[index][i]:
                return False

        return True

    def show_clusters(self):
        """
        Helper function for graphical visualization of clusters
        """

        print('\n clusters segmentation:')
        for i, cluster in enumerate(self.clusters):
            print(f"cluster: {i}, length: {len(cluster)}")

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

        for i in range(self.n_clusters):
            tmp = x_principal.iloc[self.clusters_with_candidate_idx[i]]
            plt.scatter(tmp['x'], tmp['y'])

        plt.show()

    def fit(self):
        """
        Main training procedure:

        initialize centroids

        for iteration in MAX_ITERATIONS:
            for entry in data:
                find closest cluster
                add entry to cluster

            calc new centroids.
            compare new and old centroids
            if centroids are not the same, continue to new iteration

        """

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

    def calc_inner_segmentation(self):
        """
        order clusters by company segmentation
        """
        clusters = [{} for _ in range(self.n_clusters)]

        for i, cluster in enumerate(self.clusters_with_candidate_idx):
            for can in cluster:
                label = self.order.iloc[can]['company']
                if label not in clusters[i]:
                    clusters[i][label] = [can]
                else:
                    clusters[i][label].append(can)

        return clusters

    def company_order(self, candidates: list, job_offer: dict, gender: bool = False, age: bool = False):
        """
        return a list of candidates ranked by the score or 'closeness' to the job_offer
        """
        scores = []
        job_converted = self.representation_conversion(job_offer)
        for i, candidate in enumerate(candidates):
            converted = self.representation_conversion(vars(candidate))
            scores.append([i, self.distance_calc(
                converted, job_converted, gender=gender, birth_year=age)])

        scores.sort(key=lambda score: score[1])
        return scores

    def calc_percents(self, show=True):
        """
        Calc the percent of companies in all clusters
        """
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
                sums[option] = (cluster.count(option) /
                                size * 100, cluster.count(option))

            percents[i] = sums

        self.percents = percents

        if show:
            self.print_cluster_company_percent()

    def print_cluster_company_percent(self):
        """
        utility function, prints the calculated percents to stdout
        """
        for k in self.percents:
            print(f"\n********         cluster {k + 1}:         ********")
            for row in self.percents[k]:
                print(
                    f"{row}: {self.percents[k][row][0]}, total: {self.percents[k][row][1]} ")

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
            print(
                f"correct: {c / (c + w) * 100}5, wrong: {w / (c + w) * 100}\n")
            print(precision[i])

        return precision

    def calc_precision(self, precision, label, cluster_idx):
        ordered = {k: v for k, v in sorted(
            self.percents[cluster_idx].items(), reverse=True, key=lambda item: item[1])}
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

    def predict(self, entry: dict):
        """
        Provide prediction for the given entry to which company it most fits
        """
        converted = self.representation_conversion(entry)
        cluster_idx = self.find_closest_cluster(converted, False)
        distances = []
        centroids = self.clusters_inner_centroids[cluster_idx]

        for key in centroids:
            distances.append(
                (key, self.distance_calc(converted, centroids[key])))

        return distances





def create_matrix():
    """
    utility function to create a matrix of distances between all entries
    """

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000000)
    raw_data = np.load("all.npy", allow_pickle=True)
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

    order = combined[['name', 'company']].copy()
    data = combined.copy().drop(['name', "company"], axis=1)

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
            print(
                f"total time to calculate will be: {diff.total_seconds() / 60 * size} minutes")

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

def find_inner_correlation(path):
    with open(path, 'rb') as file:
        model: Kmeans = pkl.load(file)
        model.show_clusters()

    original = program.ReadData.read_local_json_employees()

    for i, cluster in enumerate(model.clusters_with_candidate_idx):
        roles = {'name': {}, 'role': {}}

        print(f"***************** displaying cluster {i} ********************")
        for idx in cluster:
            candidate = original[original['full_name']
                                 == model.order.iloc[idx]['name']]
            positions = candidate['experience'].values

            for position in positions[0]:
                if position['current_job'] == True:
                    if position['title_name'] not in roles['name']:
                        roles['name'][position['title_name']] = 1
                    else:
                        roles['name'][position['title_name']] += 1

                    if position['title_role'] not in roles['role']:
                        roles['role'][position['title_role']] = 1
                    else:
                        roles['role'][position['title_role']] += 1

        for key in {k: v for k, v in sorted(roles["name"].items(), key=lambda item: item[1])}:
            print(f"key: {key}, amount: {roles['name'][key]}")

        for key in {k: v for k, v in sorted(roles["role"].items(), key=lambda item: item[1], reverse=True)}:
            print(f"key: {key}, amount: {roles['role'][key]}")

def calc_wcss(clusters):
    """
    clusters: a list of clusters each containing all distances in the cluster.
    """
    total = 0
    for cluster in clusters:
        total += sum([number ** 2 for number in cluster])

    return total

def calc_elbow(min_k = 2,max_k = 20 ,validation=False):
    print("starting elbow method")
    wcss = []

    for i in range(min_k, max_k):
        model = None
        if validation:
            data = load_iris(return_X_y=True)
            model : KMeans = KMeans(n_clusters=i, random_state=0).fit(data[0])
            total = model.inertia_

        else:
            model = Kmeans(i, representation=DistMethod.fix_length_freq,max_iter=20)
            model.fit()
            total = calc_wcss(model.clusters_distances)

        wcss.append(total)
        print(f"******  wcss: {wcss}")

    print("***********************")
    for i,dist in enumerate(wcss):
        print(f"K = {i + min_k}, WCSS: {dist}")

    plt.plot(range(min_k, max_k), wcss)
    plt.title("Iris data set")
    plt.xticks(range(min_k,max_k))
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()


def calc_clustering_quality(path, type=""):
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

    normalized = []

    for cluster in model.clusters_distances:
        tmp = []
        for val in cluster:
            norm = (val - _min) / (_max - _min)
            tmp.append(norm ** 2)

        normalized.append(tmp)

    sums = [sum(cluster) for cluster in normalized]

    print(f"{type} distance measure")
    print(f"total sum: {sum(sums)}\n")


def mini_batch_test(path):
    with open(path, 'rb') as file:
        model: Kmeans = pkl.load(file)
        print(len(model.data))

        test_group = []

        for cluster in model.clusters:
            group = random.sample(cluster,10)
            tmp = []
            for entry in group:
                cur = copy.deepcopy(entry)
                size = math.ceil(len(entry) * 0.025)
                indexes = random.sample(range(0,len(entry)),size)

                for index in indexes:
                    if entry[index] is not None:
                        target = math.ceil(entry[index] * 0.98)
                        if entry[index] == target:
                            cur[index] = entry[index] + 1
                        else:
                            cur[index] = target

                tmp.append(cur)

            test_group.append(tmp)


        correct = 0
        wrong = 0
        for i,group in enumerate(test_group):
            for entry in group:
                actual = model.find_closest_cluster(entry,validation=True)

                if i == actual:
                    correct += 1
                else:
                    wrong += 1

        print(100 * correct / (correct + wrong))
        return 100 * correct / (correct + wrong)


