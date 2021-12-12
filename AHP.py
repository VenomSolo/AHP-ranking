import numpy as np
from numpy.core.numeric import convolve
import os

from numpy.lib.index_tricks import nd_grid

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

alternatives = []
criterias = []
criteria_matrixes = []
eigenvectors = []

if __name__ == '__main__':

    clear()
    alt_count = int(input("Podaj ilosc alternatyw: "))
    for i in range(alt_count):
        alternatives.append(input(f"Podaj {i + 1}. alternatywe: "))

    clear()
    crit_count = int(input("Podaj ilosc kryteriów: "))
    for i in range(crit_count):
        criterias.append(input(f"Podaj {i + 1}. kryterium: "))
        criteria_matrixes.append(
            np.ones(shape=(alt_count, alt_count), dtype=float))

    for c in range(crit_count):
        criteria = criterias[c]
        for a1 in range(alt_count):
            for a2 in range(a1 + 1, alt_count):

                alt1 = alternatives[a1]
                alt2 = alternatives[a2]

                

                while True:
                    try:
                        clear()
                        print(f"Kryterium: {criteria}")
                        print(f"{alt1} VS {alt2}")

                        val1, val2 = map(float, input(">>").split(":"))
                        val = val1 / val2
                        criteria_matrixes[c][a1, a2] = val
                        criteria_matrixes[c][a2, a1] = 1 / val
                    except:
                        continue
                    break


        w, v = np.linalg.eig(criteria_matrixes[c])
        eigenvectors.append(v[:, 0] / np.linalg.norm(v[:, 0], ord=1))

        clear()
        print(f"Kryterium: {criteria}")
        print(criteria_matrixes[c])
        print(v[:, 0] / np.linalg.norm(v[:, 0], ord=1))
        input("\nKliknij Enter, aby przejść dalej...")

    critcrit_matrix = np.ones(shape=(crit_count, crit_count))

    for c1 in range(crit_count):
        for c2 in range(c1 + 1, crit_count):

            calt1 = criterias[c1]
            calt2 = criterias[c2]
            

            while True:
                    try:
                        clear()
                        print(f"{calt1} VS {calt2}")
                        val1, val2 = map(float, input(">>").split(":"))
                        val = val1 / val2
                        critcrit_matrix[c1, c2] = val
                        critcrit_matrix[c2, c1] = 1 / val
                    except:
                        continue
                    break

    print(f"Kryteria")
    print(critcrit_matrix)

    w, v = np.linalg.eig(critcrit_matrix)

    crit_eig = v[:, 0] / np.linalg.norm(v[:, 0], ord=1)

    print(crit_eig)

    ranking = np.zeros(shape=(1, alt_count), dtype=complex)

    for c in range(crit_count):
        scaled_vector = crit_eig[c] * eigenvectors[c]
        for a in range(alt_count):
            ranking[0, a] += abs(scaled_vector[a])

    input("\nKliknij Enter, aby przejść dalej...")
    clear()
    print("Ranking")

    for a in range(alt_count):
        print(f"{alternatives[a]}: {ranking[0, a]};")
