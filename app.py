from ahp import *

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


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


def gather_data(alternatives, hierarchy):
    results = {}
    for (criteria, children) in hierarchy.items():
        if children == []:
            results[criteria] = ask_for_ACM(alternatives, criteria).tolist()
    for (criteria, children) in hierarchy.items():
        if children != []:
            results[criteria] = ask_for_CCM(children).tolist()
    return results


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
    # for (expert, result) in answers:
    # print(expert + ":")
    # print(result)


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

    print(results)
    print(normalized_geometry_mean(results))


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
                print(f"{criteria}: {cons_index}")
                if cons_index > 0.1:
                    inconsistent = True
            print("Inconsistent") if inconsistent else print("Consistent")