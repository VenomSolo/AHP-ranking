import File_Processor as fp
import AHP_App as app


def criterias_to_Categories(hierarchy, criterias):
    Categories = {}
    depths = {}
    for criteria in criterias:
        depth, name = criteria
        depths[name] = depth

        if depth == 1:
            cat = fp.Category(name, depth)
            Categories[name] = cat

    def add_sub(category, criteria):
        for sub_criteria in hierarchy[criteria]:
            category.add_sub(sub_criteria, depths[sub_criteria])
            add_sub(category, sub_criteria)

    for criteria in hierarchy[0]:
        add_sub(Categories[criteria], criteria)

    return Categories.values()

def Categories_to_criterias(categories):
    return