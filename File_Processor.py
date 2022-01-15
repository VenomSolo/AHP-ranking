"""
Ten moduł odpowiada za klasę File_Processor, która zajmuje się obsługą plików.
"""
from collections import OrderedDict
import ast
from Category import Category



class File_Processor:
    """
    Klasa odpowiadająca za obsługę plików z informacjami o rankingu AHP.

    Atrybuty:
        filename: (str) nazwa pliku wejściowego z informacjami o rankingu.
    Metody:
        __init__(filename):
            Konstruktor obiektu.
        get_rest_of_line(position,data):
            Pomocnicza metoda zwracająca string z danych od podanej pozycji do końca wiersza.
        AddForm(title,alternatives,categories):
            Metoda dodająca do pliku wejściowego podane dane rankingu AHP
        RemoveForm(title):
            Metoda usuwająca z pliku wejściowego dane dla rankingu AHP o podanej nazwie
        TakeForm(title):
            Zwraca alternatywy, oraz kryteria, dla rankingu o podanej nazwie
        CheckForms():
            Zwraca listę nazw rankinków w pliku wejściowym.
        SendForm(title,expert_name,dict):
            Wpisuje do pliku wynikowego dane o wynikach rankingu o podanej nazwie dla danego eksperta
        ReadFormAnswer(title):
            Zwraca odczytane z pliku wynikowego dane o wynikach rankingu o podanej nazwie.
    """
    def __init__(self, filename):
        """
        Kontruktor tworzący obiekt FileProcessor

        :param filename:(str) Nazwa/Ścieżka bezwzględna pliku wejściowego
        """
        self.filename = filename

    def get_rest_of_line(self, position, data):
        """
        Pomocnicza metoda zbierająca tekst z danych, od pozycji początkowej do końca wiersza.

        :param position: (int) pozycja początkowa
        :param data: (str) dane, z których odczytujemy wiersz
        :return: Zwraca resztę wiersza w result, oraz pozycję końcową w position
        """
        result = ""
        while position < len(data) and data[position] != "\n":
            result += data[position]
            position += 1
        return result, position

    def AddForm(self, title, alternatives, categories):
        """
        Metoda dodająca do pliku wejściowego informacje o rankingu zgodnie z przyjętym formatem.

        :param title: (str) Nazwa dodawanego rankingu
        :param alternatives: (str[]) Lista nazw dodawanych alternatyw
        :param categories: (Category[]) Lista dodawanych kategorii
        :return: Nic nie zwraca
        """
        file = open(self.filename, "a")
        file.write("!" + title + "\n")
        for alt in alternatives:
            file.write("@" + alt + "\n")
        for cat in categories:
            file.write(cat.__str__())
        file.close()

    def RemoveForm(self, title):
        """
        Metoda usuwająca dane rankingu o podanej nazwie z pliku wejściowego.

        :param title: (str) Nazwa usuwanego rankingu
        :return: Nic nie zwraca
        """
        file = open(self.filename, "r")
        file_data = file.read(-1)
        file.close()
        start_position, end_position, position = (-1, -1, 0)
        title_found = False
        while (position < len(file_data)):
            if file_data[position] == "!":
                if title_found:
                    end_position = position
                    break
                else:
                    start_position = position
                position += 1
                found_title, position = self.get_rest_of_line(
                    position, file_data)
                if found_title == title:
                    title_found = True
            position += 1
        result = file_data[:start_position] + file_data[end_position:-1]+"\n"
        file = open(self.filename, "w")
        file.write(result.lstrip())
        file.close()

    def TakeForm(self, title):
        """
        Metoda zwracająca informacje o rankingu o podanej nazwie z pliku wejściowego.

        :param title: (str) nazwa szukanego rankingu
        :return: Zwraca listę alternatyw oraz kategorii
        """
        file = open(self.filename, "r")
        file_data = file.read(-1)
        position = 0
        alternatives = []
        categories = []
        while (position < len(file_data)):
            if file_data[position] == "!":
                position += 1
                found_title, position = self.get_rest_of_line(
                    position, file_data)
                if found_title == title:
                    position += 1
                    while position < len(
                            file_data) and file_data[position] == "@":
                        position += 1
                        alt, position = self.get_rest_of_line(
                            position, file_data)
                        alternatives.append(alt)
                        position += 1
                    while position < len(
                            file_data) and file_data[position] == "#":
                        depth = 0
                        while file_data[position] == "#":
                            depth += 1
                            position += 1
                        if depth == 1:
                            cat, position = self.get_rest_of_line(
                                position, file_data)
                            categories.append(Category(cat, 1))
                            position += 1
                        else:
                            cat, position = self.get_rest_of_line(
                                position, file_data)
                            categories[len(categories) - 1].add_sub(cat, depth)
                            position += 1
                    if position < len(
                            file_data) and file_data[position] == "!":
                        position -= 1
            position += 1
        file.close()
        return (alternatives, categories)

    def CheckForms(self):
        """
        Metoda zwracająca wszystkie nazwy rankingów z pliku wejściowego.

        :return: Zwraca listę nazw rankingów z pliku wejściowego
        """
        file = open(self.filename)
        file_data = file.read(-1)
        position = 0
        titles = []
        while position < len(file_data):
            if file_data[position] == "!":
                position += 1
                found_title, position = self.get_rest_of_line(
                    position, file_data)
                titles.append(found_title)
            position += 1
        file.close()
        return titles

    def SendForm(self, title, expert_name, dict):
        """
        Metoda zapisująca do pliku wyjściowego ([nazwa_rankingu]_result.txt) wynik rankingu dla
        danego eksperta.

        :param title: (str) nazwa rankingu AHP
        :param expert_name: (str) nazwa eksperta, który tworzył ranking
        :param dict: (dictionary) słownik z wynikami rankingu
        :return: Nic nie zwraca
        """
        file = open(title + "_result.txt", "a+")
        file.close()

        file = open(title + "_result.txt", "r")
        file_data = file.read(-1)
        position = 0
        while (position < len(file_data)):
            if file_data[position] == "$":
                position += 1
                found_expert, position = self.get_rest_of_line(
                    position, file_data)
                if found_expert == expert_name:
                    return
            position += 1
        file.close()
        file = open(title + "_result.txt", "a")
        file.write("$" + expert_name + "\n")
        for key in dict:
            if key== ("0",0):
                val=dict[key]
                file.write(str(val)+"\n")
            else:
                val = dict[key]
                for i in range(int(key[1])):
                    file.write("#")
                file.write(key[0] + "\n")
                file.write(str(val) + "\n")

        file.close()

    def ReadFormAnswer(self, title):
        """
        Metoda odczytująca odpowiedzi z pliku wyjściowego dla danego rankingu AHP.

        :param title: (str) Nazwa rankingu AHP
        :return: Zwraca listę z krotkami ([nazwa eksperta],[słownik z wynikami rankingu])
        """
        file = open(title + "_result.txt", "r")
        file_data = file.read(-1)
        position = 0
        result = []

        while (position < len(file_data)):
            if file_data[position] == "$":
                found_expert, position = self.get_rest_of_line(
                    position, file_data)
                categorie_dict = OrderedDict()

                position += 1
                cat_res, position=self.get_rest_of_line(position,file_data)
                categorie_dict[("0", 0)] = ast.literal_eval(cat_res)

                position+=1
                while position < len(file_data) and file_data[position] == "#":
                    depth = 0
                    cat = ""
                    while file_data[position] == "#":
                        depth += 1
                        position += 1

                    cat, position = self.get_rest_of_line(position, file_data)
                    position += 1
                    form_result, position = self.get_rest_of_line(
                        position, file_data)
                    position += 1
                    categorie_dict[(cat,
                                    depth)] = ast.literal_eval(form_result)
                position -= 1
                result.append((found_expert, categorie_dict))
            position += 1

        file.close()
        return result


if __name__ == '__main__':
    processor = File_Processor("test.txt")
    #taken_alt,taken_cat=processor.TakeForm("Bruh")
    #print(taken_alt)
    #print(taken_cat)
    #print(processor.CheckForms())
    test_cat = []
    test_cat.append(Category("test1", 1))
    test_cat[0].add_sub("test1.1", 2)
    test_cat[0].add_sub("test1.2", 2)
    test_cat.append(Category("test2", 1))
    test_cat.append(Category("test3", 1))
    #processor.AddForm("Bruh",["a","b","bazinga"],test_cat)
    processor.RemoveForm("Bruh")
    processor.RemoveForm("Bruh2")
    processor.RemoveForm("Example")
    processor.AddForm("Example", ["a", "b", "bazinga"], test_cat)
    # test_midman = Middleman.Categories_to_criterias(test_cat)
    # print(test_midman)

    test_dict = OrderedDict()
    test_dict[("albania", 1)] = [("safety", 0.3), ("chill", 0.5),
                                 ("poverty", 0.2)]
    test_dict[("safety", 2)] = [("police", 0.3), ("army", 0.2), ("laws", 0.5)]
    test_dict[("romania", 1)] = [("safety", 0.1), ("chill", 0.3),
                                 ("poverty", 0.6)]
    test_expert = "Ekspert"
    test_title = "expert_test"

    #print(test_dict)
    #processor.SendForm(test_title,test_expert,test_dict)
    # test_result=processor.ReadFormAnswer(test_title)
    # print(test_result)
