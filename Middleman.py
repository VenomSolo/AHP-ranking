import File_Processor as fp
from Category import Category
import AHP_App as app


def criterias_to_Categories(hierarchy, criterias):
    Categories = {}
    depths = {}
    for criteria in criterias:
        depth, name = criteria
        depths[name] = depth

        if depth == 1:
            cat = Category(name, depth)
            Categories[name] = cat

    def add_sub(category, criteria):
        for sub_criteria in hierarchy[criteria]:
            category.add_sub(sub_criteria, depths[sub_criteria])
            add_sub(category, sub_criteria)

    for criteria in hierarchy[0]:
        add_sub(Categories[criteria], criteria)

    return Categories.values()

def Categories_to_criterias(categories):
    def iterate_through_subcategorie(list,categorie):
        list.append((categorie.depth,categorie.GetName()))
        for sub_category in categorie.subcategories:
            iterate_through_subcategorie(list,sub_category)

    criterias=[]
    for categorie in categories:
        iterate_through_subcategorie(criterias,categorie)



    return criterias