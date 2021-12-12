import numpy as np
from numpy.core.numeric import convolve
import os

from numpy.lib.index_tricks import nd_grid

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

criteria_matrixes = []
eigenvectors = []


def input_alternatives():
    alternatives = []
    clear()
    alt_count = int(input("Podaj ilosc alternatyw: "))
    for i in range(alt_count):
        alternatives.append(input(f"Podaj {i + 1}. alternatywe: "))
    return alternatives


def input_criteria():

    criterias = []
    clear()
    depth = 1
    print("Podaj kryteria: ")
    while True:
        line = input(depth * "#")
        if len(line) == 0:
            op = ''
        else:
            op = line[-1]
            if len(line[:-1]) > 0:
                criterias.append((depth, line[:-1]))

        if op == '>':
            depth += 1
        elif op == '<':
            depth -= 1
        elif op == '|':
            depth = depth
        elif op == '.':
            break

    return criterias


def get_basic_criteria(criterias):
    basic = []

    last_depth = 0
    last_name = None
    for criteria in criterias:
        depth, name = criteria

        if depth >= last_depth:
            basic


def create_hierarchy(criterias):
    def find_parent(depth, index):
        for i in reversed(range(index)):
            if criterias[i][0] < depth:
                return criterias[i][1]
        return 0

    hierarchy = {name: [] for (_depth, name) in criterias}
    hierarchy[0] = []

    print(criterias)
    for i in range(len(criterias)):
        depth, name = criterias[i]
        hierarchy[find_parent(depth, i)].append(name)

    return hierarchy


def ask_for_ACM(alternatives, criteria):
    alt_count = len(alternatives)
    acm = np.ones(shape=(alt_count, alt_count), dtype=float)

    for a1 in range(alt_count):
        for a2 in range(a1 + 1, alt_count):

            alt1 = alternatives[a1]
            alt2 = alternatives[a2]

            while True:
                try:
                    clear()
                    print(f"Kryterium: {criteria}")
                    print(f"{alt1} VS {alt2}")

                    line = input(">>")
                    if len(line) == 0: break

                    val1, val2 = map(float, line.split(":"))
                    val = val1 / val2
                    acm[a1, a2] = val
                    acm[a2, a1] = 1 / val
                except:
                    continue
                break
    return acm


def ask_for_CCM(criterias):
    return ask_for_ACM(criterias, "criteria importance")
    pass


def normalized_eigenvector(comparison_matrix):
    w, v = np.linalg.eig(comparison_matrix)
    return v[:, 0] / np.linalg.norm(v[:, 0], ord=1)


def rank_flat(ccm_eigenvector, acm_eigenvectors):
    crit_count = len(ccm_eigenvector)
    alt_count = len(acm_eigenvectors[0])
    ranking = np.zeros(shape=(1, alt_count), dtype=complex)

    for c in range(crit_count):
        scaled_vector = ccm_eigenvector[c] * acm_eigenvectors[c]
        for a in range(alt_count):
            ranking[0, a] += abs(scaled_vector[a])

    return ranking


def gather_data(alternatives, hierarchy):
    results = {}
    for (criteria, children) in hierarchy.items():
        if children == []:
            results[criteria] = normalized_eigenvector(
                ask_for_ACM(alternatives, criteria))
    for (criteria, children) in hierarchy.items():
        if children != []:
            results[criteria + "_sub"] = normalized_eigenvector(
                ask_for_CCM(children))
    print(results)
    return results


def _rank_hierarchy(alternatives, hierarchy, criteria, data):
    print(criteria)
    subcriteria = hierarchy[criteria]
    if subcriteria == []:
        return data[criteria]

    subcriteria_priority = data[criteria + "_sub"]
    subcriteria_eigenvector = normalized_eigenvector(subcriteria_priority)

    alt_count = len(alternatives)
    subcrit_count = len(subcriteria)
    ranking = np.zeros(shape=(1, alt_count), dtype=complex)
    for i in range(alt_count):

        for j in range(subcrit_count):
            res = _rank_hierarchy(alternatives, hierarchy, subcriteria[j],
                                  data)
            #print(res)
            ranking[0, i] += (subcriteria_eigenvector[j] * res[i])
    print("ranking", ranking)
    return ranking[0]

    pass


def rank_hierarchy(alternatives, criterias):
    hierarchy = create_hierarchy(criterias)
    data = gather_data(alternatives, hierarchy)
    return _rank_hierarchy(alternatives, hierarchy, 0, data)
