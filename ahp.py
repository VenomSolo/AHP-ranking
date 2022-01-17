from collections import OrderedDict
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import convolve
import os
from enum import Enum
import File_Processor as fp
import Middleman as md
import random
import math

from numpy.lib.index_tricks import nd_grid

INF = 2e100


class Method(Enum):
    EVM = 1,
    GMM = 2


methods = {"EVM": Method.EVM, "GMM": Method.GMM}


class Hierarchy:
    def __init__(self):
        self.h = {"root": []}
        pass

    def add_category(self, name, parent="root"):
        self.h[parent].append(name)

    def rank_data(self, data, method):
        for (criteria, result) in data.items():
            result = prepare_complete_auxilary_matrix(result)
            if method == Method.EVM:
                data[criteria] = normalized_eigenvector(result)
            if method == Method.GMM:
                data[criteria] = normalized_geometry_mean(result)


def create_hierarchy(criterias):
    def find_parent(depth, index):
        for i in reversed(range(index)):
            if criterias[i][0] < depth:
                return criterias[i][1]
        return 0

    hierarchy = {name: [] for (_depth, name) in criterias}
    hierarchy[0] = []

    for i in range(len(criterias)):
        depth, name = criterias[i]
        hierarchy[find_parent(depth, i)].append(name)

    return hierarchy


#add marker
def is_incomplete(matrix):
    for row in matrix:
        for val in row:
            if val == INF:
                return True
    return False


#for EVM
def prepare_complete_auxilary_matrix(matrix):
    if not is_incomplete(matrix):
        return matrix
    print(matrix)
    l = len(matrix)
    new_matrix = np.zeros(shape=(l, l), dtype=float)
    for row in range(l):
        for col in range(l):
            val = matrix[row][col]
            if val != INF:
                new_matrix[row][col] += val
            else:
                new_matrix[row][row] += 1
    print(new_matrix)
    return new_matrix.tolist()


def normalized_eigenvector(comparison_matrix):
    w, v = np.linalg.eig(comparison_matrix)
    return normalize_vector(np.abs(v[:, 0]))


def consistency_index(comparison_matrix):
    w = np.linalg.eigvals(comparison_matrix)
    return (max(w) - len(comparison_matrix)) / (len(comparison_matrix) - 1)


def _simulate_random_index(scale, matrix_size):
    sim_size = 50
    sum_of_sim = 0
    for i in range(sim_size):
        test_matrix = np.diag(np.ones(matrix_size))
        for j in range(matrix_size):
            for k in range(j + 1, matrix_size):
                test_matrix[j, k] = random.randrange(1, scale + 1)
                test_matrix[k, j] = 1 / test_matrix[j, k]
        sum_of_sim += consistency_index(test_matrix)
    return sum_of_sim / sim_size


def consistency_ratio(comparison_matrix):
    return consistency_index(comparison_matrix) / _simulate_random_index(
        np.amax(comparison_matrix), len(comparison_matrix))


def geometric_consistency_index(comparison_matrix):
    sum_of_e = 0
    alt_priorities = normalized_eigenvector(comparison_matrix)
    for i in range(len(comparison_matrix)):
        for j in range(i + 1, len(comparison_matrix)):
            sum_of_e += math.log(comparison_matrix[i, j] * alt_priorities[j] /
                                 alt_priorities[i])**2
    return (2 / ((len(comparison_matrix) - 1) *
                 (len(comparison_matrix) - 2))) * sum_of_e


def normalized_geometry_mean(comparison_matrix):
    alt_count = len(comparison_matrix)
    ranking = np.ones(shape=(1, alt_count), dtype=complex)
    for row in range(alt_count):
        for val in comparison_matrix[row]:
            ranking[0, row] *= val
        ranking[0, row] **= (1 / alt_count)
    return normalize_vector(ranking[0])


def normalize_vector(vector):
    return vector / np.linalg.norm(vector, ord=1)


def rank_flat(ccm_eigenvector, acm_eigenvectors):
    crit_count = len(ccm_eigenvector)
    alt_count = len(acm_eigenvectors[0])
    ranking = np.zeros(shape=(1, alt_count), dtype=complex)

    for c in range(crit_count):
        scaled_vector = ccm_eigenvector[c] * acm_eigenvectors[c]
        for a in range(alt_count):
            ranking[0, a] += abs(scaled_vector[a])

    return ranking[0]


def rank_data(data, method):
    for (criteria, result) in data.items():
        result = prepare_complete_auxilary_matrix(result)
        if method == Method.EVM:
            data[criteria] = normalized_eigenvector(result)
        if method == Method.GMM:
            data[criteria] = normalized_geometry_mean(result)


def _rank_hierarchy(alternatives, hierarchy, criteria, data):
    subcriteria = hierarchy[criteria]
    if subcriteria == []:
        return data[criteria]

    subcriteria_priority = data[criteria]

    alt_count = len(alternatives)
    subcrit_count = len(subcriteria)
    ranking = np.zeros(shape=(1, alt_count), dtype=complex)

    for i in range(alt_count):
        for j in range(subcrit_count):
            result = _rank_hierarchy(alternatives, hierarchy, subcriteria[j],
                                     data)
            ranking[0, i] += (subcriteria_priority[j] * result[i])
            #print(subcriteria_priority[j], result[i])

    return ranking[0]