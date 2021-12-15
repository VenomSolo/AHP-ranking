from typing import OrderedDict
import numpy as np
from numpy.core.numeric import convolve
import os
from enum import Enum
import File_Processor as fp
import Middleman as md

from numpy.lib.index_tricks import nd_grid

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

criteria_matrixes = []
eigenvectors = []


class Method(Enum):
    EVM = 1,
    GMM = 2


def input_title():
    return input("Podaj tytul: ")


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
    return normalize_vector(v[0])


def normalized_geometry_mean(comparison_matrix):
    alt_count = len(comparison_matrix)
    ranking = np.ones(shape=(1, alt_count), dtype=complex)
    for row in range(alt_count):
        for val in row:
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


def gather_data(alternatives, hierarchy):
    results = {}
    for (criteria, children) in hierarchy.items():
        if children == []:
            results[criteria] = ask_for_ACM(alternatives, criteria).tolist()
    for (criteria, children) in hierarchy.items():
        if children != []:
            results[criteria] = ask_for_CCM(children).tolist()
    print(results)
    return results


def rank_data(data, method):
    for (criteria, result) in data:
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

    return ranking[0]
    pass


def create_proc(server):
    return fp.File_Processor(server)


def rank_hierarchy(alternatives, criterias, method):
    hierarchy = create_hierarchy(criterias)
    data = gather_data(alternatives, hierarchy)
    ranked_data = rank_data(data, method)
    return _rank_hierarchy(alternatives, hierarchy, 0, ranked_data)


def check_forms(server):
    f_processor = create_proc(server)
    return f_processor.CheckForms()


def take_form(server, title, username):
    f_processor = create_proc(server)
    (alt, cat) = f_processor.TakeForm(title)
    criterias = md.Categories_to_criterias(cat)
    hierarchy = create_hierarchy(criterias)
    data = gather_data(alt, hierarchy)
    print(criterias)
    data_with_depth = OrderedDict()
    #print(data)
    data_with_depth[("0", 0)] = data[0]
    for (criteria, result) in data.items():
        for crit in criterias:
            if crit[1] == criteria:
                data_with_depth[(criteria, crit[0])] = result
    print(data_with_depth)
    f_processor.SendForm(title, username, data_with_depth)
    return


def add_form(server, title):
    f_processor = create_proc(server)
    alt = input_alternatives()
    crit = input_criteria()
    hier = create_hierarchy(crit)
    f_processor.AddForm(title, alt, md.criterias_to_Categories(hier, crit))


def remove_form(server, title):
    f_processor = create_proc(server)
    f_processor.RemoveForm(title)


def read_form(server, title):
    f_processor = create_proc(server)
    answers = f_processor.ReadFormAnswer(title)
    for (expert, result) in answers:
        print(expert + ":")
        print(result)