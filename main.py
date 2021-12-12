import Middleman as mm
import File_Processor as fp
import AHP_App as app

if __name__ == '__main__':

    # v = [
    # -0.02964209 + 0.j, -0.13897508 + 0.j, -0.24771773 + 0.j,
    # -0.0452891 + 0.j
    # ]
    # print(v / -np.linalg.norm(v, ord=1))

    processor = fp.File_Processor("test.txt")
    alt = app.input_alternatives()
    crit = app.input_criteria()
    hierarchy = app.create_hierarchy(crit)
    categories = mm.criterias_to_Categories(hierarchy, crit)
    print(categories)
    processor.AddForm("test", alt, categories)
    # hierarchy = create_hierarchy(crit)
    # print(hierarchy)
    # ranking = rank_hierarchy(alt, crit)
    # print(ranking)
