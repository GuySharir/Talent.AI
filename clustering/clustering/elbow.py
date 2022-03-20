import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, normalize, StandardScaler
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import matplotlib.cm as cm
from termcolor import colored


def find_k_elbow(data: pd.DataFrame, range_start: int, range_end: int) -> None:
    k_options = range(range_start, range_end)

    Sum_of_squared_distances = []
    for k in k_options:
        km = KMeans(n_clusters=k, n_init=20)

        km = km.fit(data)
        print(km.labels_)
        Sum_of_squared_distances.append(km.inertia_)

    plt.plot(k_options, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title(f'Elbow Method For Optimal k')
    plt.show()


def reduce_dimension(data: pd.DataFrame) -> pd.DataFrame:
    # reduce dimension to 2 in order to visoallize silouett
    pca = PCA(n_components=2)
    X_principal = pca.fit_transform(data)
    X_principal = pd.DataFrame(X_principal)
    X_principal.columns = ['p1', 'p2']
    return X_principal


def find_k_silhouette(data: pd.DataFrame, range_start: int, range_end: int, full: bool,
                      mid_plots: bool = False) -> None:
    # helper inner function
    SelBest = lambda arr, x: arr[np.argsort(arr)[:x]]

    data = reduce_dimension(data)

    range_n_clusters = range(range_start, range_end)

    if full:
        best_sil = []
        for n_clusters in range_n_clusters:
            # Create a subplot with 1 row and 2 columns
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.set_size_inches(18, 7)

            # The 1st subplot is the silhouette plot
            # The silhouette coefficient can range from -1, 1
            ax1.set_xlim([-1, 1])

            # The (n_clusters+1)*10 is for inserting blank space between silhouette
            # plots of individual clusters, to demarcate them clearly.
            ax1.set_ylim([0, len(data) + (n_clusters + 1) * 10])

            # Initialize the clusterer with n_clusters value and a random generator
            # seed of 10 for reproducibility.
            clusterer = KMeans(n_clusters=n_clusters)
            cluster_labels = clusterer.fit_predict(data)

            # The silhouette_score gives the average value for all the samples.
            # This gives a perspective into the density and separation of the formed
            # clusters
            silhouette_avg = silhouette_score(data, cluster_labels)
            # print("For", n_clusters, " clusters: The average silhouette_score is :", silhouette_avg)

            best_sil.append((n_clusters, silhouette_avg))

            # Compute the silhouette scores for each sample
            sample_silhouette_values = silhouette_samples(data, cluster_labels)

            y_lower = 10
            for i in range(n_clusters):
                # Aggregate the silhouette scores for samples belonging to
                # cluster i, and sort them
                ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
                ith_cluster_silhouette_values.sort()
                size_cluster_i = ith_cluster_silhouette_values.shape[0]
                y_upper = y_lower + size_cluster_i

                color = cm.nipy_spectral(float(i) / n_clusters)
                ax1.fill_betweenx(
                    np.arange(y_lower, y_upper),
                    0,
                    ith_cluster_silhouette_values,
                    facecolor=color,
                    edgecolor=color,
                    alpha=0.7,
                )

                # Label the silhouette plots with their cluster numbers at the middle
                ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

                # Compute the new y_lower for next plot
                y_lower = y_upper + 10  # 10 for the 0 samples

            ax1.set_title("The silhouette plot for the various clusters.")
            ax1.set_xlabel("The silhouette coefficient values")
            ax1.set_ylabel("Cluster label")

            # The vertical line for average silhouette score of all the values
            ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

            ax1.set_yticks([])  # Clear the yaxis labels / ticks
            ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

            # 2nd Plot showing the actual clusters formed
            colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
            ax2.scatter(
                data['p1'].values, data['p2'].values, marker=".", s=30, lw=0, alpha=0.7, c=colors, edgecolor="k"
            )

            # Labeling the clusters
            centers = clusterer.cluster_centers_
            # Draw white circles at cluster centers
            ax2.scatter(
                centers[:, 0],
                centers[:, 1],
                marker="o",
                c="white",
                alpha=1,
                s=200,
                edgecolor="k",
            )

            for i, c in enumerate(centers):
                ax2.scatter(c[0], c[1], marker="$%d$" % i, alpha=1, s=50, edgecolor="k")

            ax2.set_title("The visualization of the clustered data.")
            ax2.set_xlabel("Feature space for the 1st feature")
            ax2.set_ylabel("Feature space for the 2nd feature")

            plt.suptitle(
                "Silhouette analysis for KMeans clustering on sample data with n_clusters = %d"
                % n_clusters,
                fontsize=14,
                fontweight="bold",
            )

        plt.show()

        best_sil.sort(key=lambda tup: tup[1], reverse=True)
        for tup in best_sil:
            print(colored(f"for {tup[0]} clusters - score: {tup[1]}", "green"))

    else:
        sils = []
        sils_err = []
        iterations = 20
        for n in range_n_clusters:
            tmp_sil = []
            flag = True
            for _ in range(iterations):
                # gmm = GaussianMixture(n, n_init=2).fit(X_principal)
                kmeans = KMeans(n_clusters=n).fit(data)
                # labels = gmm.predict(data)
                labels = kmeans.predict(data)
                sil = silhouette_score(data, labels, metric='euclidean')
                tmp_sil.append(sil)
                if flag and mid_plots:
                    plt.scatter(data['p1'], data['p2'], c=labels)
                    plt.title(f"number of clusters: {n}")
                    plt.show()
                    flag = False

            val = np.mean(SelBest(np.array(tmp_sil), int(iterations / 5)))
            err = np.std(tmp_sil)
            sils.append(val)
            sils_err.append(err)
            flag = True

        plt.errorbar(range_n_clusters, sils, yerr=sils_err)
        plt.title("Silhouette Scores", fontsize=20)
        plt.xticks(range_n_clusters)
        plt.xlabel("N. of clusters")
        plt.ylabel("Score")
        plt.show()


def load_data(path) -> pd.DataFrame:
    raw_df = np.load(path)
    raw_df = pd.DataFrame(raw_df)
    # return shuffle(raw_df)
    return raw_df


def normalize_data(data) -> pd.DataFrame:
    return normalize(data)


def scale_data(data: pd.DataFrame, scalerType: str) -> pd.DataFrame:
    if scalerType == "standard":
        scaler = StandardScaler()
        return scaler.fit_transform(data)

    if scalerType == "minmax":
        mms = MinMaxScaler()
        return mms.fit_transform(data)

    print(f"option: {scalerType} is not recognized. returning original df")
    return data


def my_kmeans(n_clusters):
    data = load_data('five.npy')
    order = np.load('fiveOrderCompany.npy')
    order = pd.DataFrame(order)
    order.rename(columns={0: "name", 1: "company"}, inplace=True)

    data = scale_data(data, "minmax")
    # data = scale_data(data, "standard")
    data = normalize_data(data)
    # data = reduce_dimension(data)
    data = pd.concat([data, order], axis=1)

    data = shuffle(data)

    train = data.iloc[0:380]
    test = data.iloc[381:-1]

    train = train.drop(['name', 'company'], axis=1)

    test_x = test.copy().drop(['name', 'company'], axis=1)
    test_y = test.copy().drop(['p1', 'p2'], axis=1)

    clusters = [[] for _ in range(n_clusters)]

    kmeans = KMeans(n_clusters=n_clusters).fit(train)
    labels = kmeans.labels_

    for i, label in enumerate(labels):
        clusters[label].append(order.iloc[i][1])

    names = {}

    for i, cluster in enumerate(clusters):
        partition = {}
        for label in cluster:
            if label not in partition:
                partition[label] = 1
            else:
                partition[label] += 1
        print(f"\ncluster number {i}")
        size = len(cluster)

        max_key = ''
        max_val = -1

        for key in partition:
            print(f"{key}: {partition[key] / size}")
            if partition[key] / size > max_val:
                max_val = partition[key] / size
                max_key = key

        names[i] = max_key

        print('\n')

    print(names)
    print("************************************")

    predictions = kmeans.predict(test_x)

    mem = {}

    good = 0
    bad = 0

    for i, pred in enumerate(predictions):
        if pred in names:
            if test_y.iloc[i]['company'] == names[pred]:
                good += 1
            else:
                bad += 1

    print(f"correct: {good}, incorrect: {bad}")
    #     if pred not in mem:
    #         mem[pred] = {}
    #
    #     if test_y.iloc[i]['company'] not in mem[pred]:
    #         mem[pred][test_y.iloc[i]['company']] = 1
    #     else:
    #         mem[pred][test_y.iloc[i]['company']] += 1
    #
    # for key in mem:
    #     print(f"label: {key}")
    #     print(mem[key])


if __name__ == '__main__':
    # data = load_data('five.npy')
    # # data = scale_data(data, "minmax")
    # data = scale_data(data, "standard")
    # data = normalize_data(data)
    # # data = reduce_dimension(data)
    #
    # find_k_elbow(data, 2, 11)
    # find_k_silhouette(data, 2, 11, True)

    my_kmeans(5)

    # order = np.load('fiveOrderCompany.npy')
    # order = pd.DataFrame(order)
    #
    # order.rename(columns={0: "name", 1: "company"}, inplace=True)
    #
    # print(order)
