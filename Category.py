"""
Ten moduł odpowiada w pełni za klasę Category, przechowującą informację o kategoriach przy obsłudze plików.
"""
class Category:
    """
    Klasa Category przechowuje informacje o kryteriach rankingu AHP takie jak nazwa, ich głębokość, oraz ich podkategorie.

    Atrybuty:
        cat_name: (str) Nazwa kategorii/kryterium.
        depth: (int) Głębokość zagnieżdżenia kategorii.
        subcategories: lista podkryteriów jako obiektów Category.

    Metody:
        __init__(name,depth)
            Konstruktor obiektu.
        GetName()
            Getter nazwy obiektu.
        find_sub(name,depth)
            Wyszukuje podkategorię o podanej nazwie i głębokości.
        add_sub(name,depth)
            Dodaje podkategorię o podanej nazwie i głębokości do najnowszej kategorii znajdującej się poziom wyżej.
        textify()
            Metoda pomocnicza wypisująca obiekt jako string sformatowany dla metod FileProcessor
    """
    def __init__(self, name, depth):
        """
        Konstruktor tworzący nowy obiekt Category.



        :param name: (str) Nazwa kategorii/kryterium
        :param depth: (int) Głębokość zagnieżdżenia kategorii
        """
        self.cat_name = name
        self.depth = depth
        self.subcategories = []

    def GetName(self):
        """
        Metoda zwracająca nazwę kryterium w obiekcie.

        :return: Zwraca string z nazwą kryterium
        """
        return self.cat_name

    def find_sub(self, name, depth):
        """
        Metoda zwracająca podkategorię na danej nazwie i głębokości

        :param name: (str) nazwa szukanej podkategorii
        :param depth: (int) głębokość szukanej podkategorii
        :return: Obiekt Category, jeżeli została znaleziona. Jeżeli nie to None.
        """
        if depth == self.depth + 1:
            for sub_cat in self.subcategories:
                if sub_cat.GetName() == name:
                    return sub_cat
        if depth > self.depth + 1:
            for sub_cat in self.subcategories:
                if not sub_cat.find_sub(name, depth) is None:
                    return sub_cat

        return None

    def add_sub(self, name, depth):
        """
        Metoda dodająca nową podkategorię o zadanej głębokości i nazwie.
        Dodawana jest do najnowszej kategorii na głębokości o 1 niższej od zadanej.

        :param name: (str) Nazwa dodawanej podkategorii
        :param depth: (int) Głębokość, na której ma być dodana podkategoria
        :return: Nic nie zwraca.
        """
        if depth < 1: return
        if depth == self.depth + 1:
            self.subcategories.append(Category(name, depth))
        else:
            if len(self.subcategories)==0: return
            self.subcategories[len(self.subcategories) - 1].add_sub(
                name, depth)

    def textify(self):
        """
        Metoda zwracająca tekstowy zapis obiektu o formacie:
        [#*depth]+[cat_name] np.
        dla cat_name = 'kategoria' i depth = 2
        zwróci: ##kategoria

        :return: (str) zwraca zapis tekstowy obiektu.
        """
        result = ""
        for i in range(self.depth):
            result += "#"

        return result + self.cat_name

    def __str__(self):
        result = ""
        result += self.textify() + "\n"
        for sub_cat in self.subcategories:
            result += sub_cat.__str__()
        return result