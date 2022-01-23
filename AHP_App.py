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
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

criteria_matrixes = []
eigenvectors = []


class Method(Enum):
    EVM = 1,
    GMM = 2


methods = {"EVM": Method.EVM, "GMM": Method.GMM}


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
    print("""End line with > to move deeper into hierarchy tree.
End line with < to return higher into hierarchy tree.
End line with | to stay on the same level in hierarchy tree.
End line with . to end defining hierarchy tree.
    """)
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

    for i in range(len(criterias)):
        depth, name = criterias[i]
        hierarchy[find_parent(depth, i)].append(name)

    return hierarchy


def is_incomplete(matrix):
    for row in matrix:
        for val in row:
            if val == INF:
                return True
    return False


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
                    print(f"Criteria: {criteria}")
                    print(
                        f"{alt1} VS {alt2} (leave input field empty and click enter to skip)"
                    )

                    line = input(">>")
                    if len(line) == 0:
                        acm[a1, a2] = INF
                        acm[a2, a1] = INF
                    else:
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


def prepare_complete_auxilary_matrix_EVM(matrix):
    if not is_incomplete(matrix):
        return matrix
    l = len(matrix)
    new_matrix = np.zeros(shape=(l, l), dtype=float)
    for row in range(l):
        for col in range(l):
            val = matrix[row][col]
            if val != INF:
                new_matrix[row][col] += val
            else:
                new_matrix[row][row] += 1

    return new_matrix.tolist()


def normalized_geometry_mean_incomplete(matrix):
    if not is_incomplete(matrix):
        return matrix
    l = len(matrix)

    cprim = np.zeros(shape=(l, 1), dtype=float)

    new_matrix = np.zeros(shape=(l, l), dtype=float)
    for row in range(l):
        for col in range(l):
            val = matrix[row][col]
            if val != INF:
                new_matrix[row][col] += 0
                cprim[row][0] += np.log(val)
            else:
                new_matrix[row][row] += 1
                new_matrix[row][col] += 1

    for row in range(l):
        new_matrix[row][row] = l - new_matrix[row][row]

    print("new matrix")
    print(new_matrix)

    vprim = np.linalg.solve(new_matrix, cprim)
    rank = np.exp(vprim)

    return normalize_vector(rank)


def normalized_eigenvector(comparison_matrix):
    w, v = np.linalg.eig(comparison_matrix)
    return normalize_vector(np.abs(v[:, 0]))


def consistency_index(comparison_matrix):
    w = np.linalg.eigvals(comparison_matrix)
    return (max(w) - len(comparison_matrix)) / (len(comparison_matrix) - 1)


def simulate_random_index(scale, matrix_size):
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
    return consistency_index(comparison_matrix) / simulate_random_index(
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
    if is_incomplete(comparison_matrix):
        return normalized_geometry_mean_incomplete(comparison_matrix)
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


def gather_data(alternatives, hierarchy):
    results = {}
    for (criteria, children) in hierarchy.items():
        if children == []:
            results[criteria] = ask_for_ACM(alternatives, criteria).tolist()
    for (criteria, children) in hierarchy.items():
        if children != []:
            results[criteria] = ask_for_CCM(children).tolist()
    return results


def rank_data(data, method):
    for (criteria, result) in data.items():
        if method == Method.EVM:
            result = prepare_complete_auxilary_matrix_EVM(result)
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
    pass


def create_proc(server):
    return fp.File_Processor(server)


def rank_hierarchy(alternatives, criterias, data, method):
    hierarchy = create_hierarchy(criterias)
    rank_data(data, method)
    return _rank_hierarchy(alternatives, hierarchy, 0, data)


def check_forms(server):
    f_processor = create_proc(server)
    return f_processor.CheckForms()


def take_form(server, title, username):
    f_processor = create_proc(server)
    (alt, cat) = f_processor.TakeForm(title)
    criterias = md.Categories_to_criterias(cat)
    hierarchy = create_hierarchy(criterias)
    data = gather_data(alt, hierarchy)
    data_with_depth = OrderedDict()
    #print(data)
    data_with_depth[("0", 0)] = data[0]
    for (criteria, result) in data.items():
        for crit in criterias:
            if crit[1] == criteria:
                data_with_depth[(criteria, crit[0])] = result
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
        for (crit, matrix) in result.items():
            print(crit[0] if crit[0] != '0' else "Root")
            for row in matrix:
                print(row)


def rank_form(server, title, method):
    f_processor = create_proc(server)
    expert_data_list = f_processor.ReadFormAnswer(title)
    expert_data = {}
    for (expert, data) in expert_data_list:
        corrected_dict = {}
        for (key, val) in data.items():
            if key[0] == "0":
                corrected_dict[0] = val
            else:
                corrected_dict[key[0]] = val
        expert_data[expert] = corrected_dict
    (alt, cat) = f_processor.TakeForm(title)
    criterias = md.Categories_to_criterias(cat)
    # print(
    # rank_hierarchy(alt, criterias, expert_data["$venom"], methods[method]))

    results = np.zeros(shape=(len(alt), len(expert_data.keys())),
                       dtype=complex)
    i = 0
    for (expert, data) in expert_data.items():
        results[:, i] = rank_hierarchy(alt, criterias, data, methods[method])
        i += 1

    results = normalized_geometry_mean(results)
    i = 1
    for (a, r) in reversed(sorted(list(zip(alt, results)),
                                  key=lambda x: x[1])):
        print(f"{i}. miejsce: {a} ({np.real(r)})")
        i += 1


def get_experts(server, title):
    f_processor = create_proc(server)
    answers = f_processor.ReadFormAnswer(title)
    for (expert, result) in answers:
        print(expert)


def check_consistency(server, title, target_expert):
    f_processor = create_proc(server)
    answers = f_processor.ReadFormAnswer(title)
    inconsistent = False
    for (expert, result) in answers:
        if expert == target_expert:
            for (criteria, table) in result.items():
                cons_index = consistency_index(table)
                crit = criteria[0] if criteria[0] != '0' else "Root"
                print(f"{crit}: {np.real(cons_index)}")
                if cons_index > 0.1:
                    inconsistent = True
            print("Inconsistent") if inconsistent else print("Consistent")
