import json
import numpy as np
import random
import pickle as pkl
import pygad as pygad
from program.DistEnum import DistMethod
from clustering.kMeans import Kmeans
from program.ReadData import set_path


class GeneticAlgPrep:
    def __init__(self):
        self.num_of_duplicates = 5
        self.records_index = 0
        self.clusters_index_list = []
        self.name_placeholder = 'laura gao'
        self.company_placeholder = 'twitter'
        self.clusters = 8

    """
        Generate 5 record duplicates with minor changes in a single attribute
        and save those records in the same cluster as the original record 
    """
    def generate_duplicates_records(self, record: list, result: list) -> list:
        attr = "job_title"
        attr_index = 7

        with open("../dataTool/frequencies/attributes_frequency.json") as f:
            df = json.load(f)
            max_freq_val = max(df[attr].values())

        records_index_per_cluster = [self.records_index]
        for i in range(self.num_of_duplicates):

            self.records_index += 1

            record_copy = record.copy()
            record_copy[attr_index] = random.randint(1, max_freq_val)
            result.append({self.name_placeholder: (self.company_placeholder, record_copy)})
            records_index_per_cluster.append(self.records_index)

        self.records_index += 1
        return records_index_per_cluster

    """
        Create small model that contains 1 record and 5 duplicates from each
        cluster in the original model
    """
    def create_small_model(self):
        with open("../clustering/demo2.pkl", "rb") as file:
            model: Kmeans = pkl.load(file)

            df_converted = set_path('dataTool/df_genetic_alg.npy')
            result = []

            for cluster_num in range(len(model.clusters)):
                rand_index = random.randint(0, len(model.clusters[cluster_num]) - 1)
                record = model.clusters[cluster_num][rand_index]

                result.append({self.name_placeholder: (self.company_placeholder, record)})
                self.clusters_index_list.append(self.generate_duplicates_records(record=record, result=result))

            print(self.clusters_index_list)
            print(result)
            np.save(df_converted, result)

            with open(set_path('dataTool/clusters_index_list.txt'), 'wb') as fp:
                pkl.dump(self.clusters_index_list, fp)

            # find average record per cluster
            print(model.clusters_with_candidate_idx)
            average_records_per_cluster = 0
            for cluster in model.clusters_with_candidate_idx:
                average_records_per_cluster += len(cluster)
            print(average_records_per_cluster / self.clusters)


def fitness_function(solution, solution_idx):
    """
    Finding number of cluster conflicts.
    We want to minimize the number of conflicts
    """
    theta1, theta2, beta, gama = solution[0], solution[1], solution[2], solution[3]

    x = Kmeans(n_clusters=8, representation=DistMethod.fix_length_freq)
    x.set_hyper_params(t1=theta1, t2=theta2, beta=beta, gama=gama)
    x.fit()

    # indicates the number of records that belongs to their correct cluster number
    fitness = 0

    with open('../dataTool/clusters_index_list.txt', 'rb') as filehandle:
        clusters_index_list = pkl.load(filehandle)
    print(clusters_index_list)
    print(x.clusters_with_candidate_idx)

    for index, cluster in enumerate(clusters_index_list):
        for record_index in cluster:
            if record_index in x.clusters_with_candidate_idx[index]:
                fitness += 1

    print(fitness)
    return fitness


def run_alg():
    num_generations = 50
    num_parents_mating = 2

    sol_per_pop = 4    # Each population has 4 solution
    num_genes = 4      # Each solution has 4 genes (theta1, theta2, gama, beta)

    gene_type = [int, int, float, float]
    #              theta1                    theta2                    gama                   beta
    gene_space = [{'low': 1, 'high': 1000}, {'low': 1, 'high': 1000}, {'low': 0, 'high': 1}, {'low': 0, 'high': 1}]
    theta1, theta2, beta, gama = 3, 10, 0.05, 0.01
    initial_population = [[theta1, theta2, beta, gama],
                          [4, 12, 0.07, 0.09],
                          [3, 11, 0.06, 0.02],
                          [4, 13, 0.07, 0.06]]

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           fitness_func=fitness_function,
                           mutation_type="random",
                           mutation_probability=0.1,
                           mutation_by_replacement=True,
                           random_mutation_min_val=0,
                           initial_population=initial_population,
                           gene_type=gene_type,
                           gene_space=gene_space)

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))


if __name__ == '__main__':
    # data initialization

    # c = GeneticAlgPrep()
    # c.create_small_model()

    run_alg()

