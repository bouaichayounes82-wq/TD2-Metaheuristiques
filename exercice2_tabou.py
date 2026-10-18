import random
from collections import deque


# ==========================================================
# TD n°2 - Exercice 2
# Recherche Taboue - Probleme de transport
# ==========================================================

# Couts de transport
#          M1  M2  M3
# D1        5   3   4
# D2        6   7   2

couts = [
    [5, 3, 4],
    [6, 7, 2]
]

# Capacites des depots
offres = [8, 9]

# Demandes des magasins
demandes = [4, 5, 8]


def calculer_cout(solution):
    """
    solution = [x1, x2, x3]
    xj = quantite envoyee par D1 vers Mj.

    D2 fournit automatiquement le complement de chaque demande.
    """
    x1 = solution

    x2 = [
        demandes[0] - x1[0],
        demandes[1] - x1[1],
        demandes[2] - x1[2]
    ]

    cout_total = 0

    for j in range(3):
        cout_total += x1[j] * couts[0][j]
        cout_total += x2[j] * couts[1][j]

    return cout_total


def solution_valide(solution):
    """
    Verifie les contraintes :
    - D1 doit livrer exactement 8 containers.
    - Aucune livraison ne doit depasser la demande.
    - D2 doit livrer exactement 9 containers.
    """
    x1 = solution

    if sum(x1) != offres[0]:
        return False

    for j in range(3):
        if x1[j] < 0 or x1[j] > demandes[j]:
            return False

    x2 = [
        demandes[0] - x1[0],
        demandes[1] - x1[1],
        demandes[2] - x1[2]
    ]

    if sum(x2) != offres[1]:
        return False

    return True


def generer_solution_aleatoire():
    """
    Genere une solution initiale faisable.
    """
    while True:
        solution = [
            random.randint(0, demandes[0]),
            random.randint(0, demandes[1]),
            random.randint(0, demandes[2])
        ]

        if solution_valide(solution):
            return solution


def generer_voisins(solution):
    """
    Un voisin est obtenu en deplacant 1 container
    de D1 d'un magasin vers un autre.
    """
    voisins = []

    for i in range(3):
        for j in range(3):

            if i == j:
                continue

            if solution[i] > 0 and solution[j] < demandes[j]:

                voisin = solution[:]

                voisin[i] -= 1
                voisin[j] += 1

                if solution_valide(voisin):
                    voisins.append(voisin)

    return voisins


def tabou_search(nombre_iterations, taille_tabou):
    """
    Recherche taboue.
    """
    solution_actuelle = generer_solution_aleatoire()

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_cout(solution_actuelle)

    tabou_list = deque(maxlen=taille_tabou)

    for _ in range(nombre_iterations):

        voisins = generer_voisins(solution_actuelle)

        # Suppression des solutions presentes dans la liste taboue
        voisins = [
            voisin for voisin in voisins
            if voisin not in tabou_list
        ]

        if not voisins:
            break

        solution_actuelle = min(
            voisins,
            key=lambda x: calculer_cout(x)
        )

        distance_actuelle = calculer_cout(solution_actuelle)

        tabou_list.append(solution_actuelle[:])

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance


# ==========================================================
# Programme principal
# ==========================================================

random.seed(42)

nombre_iterations = 100
taille_tabou = 10

meilleure_solution, meilleure_distance = tabou_search(
    nombre_iterations,
    taille_tabou
)

x1 = meilleure_solution

x2 = [
    demandes[0] - x1[0],
    demandes[1] - x1[1],
    demandes[2] - x1[2]
]

print("=" * 55)
print("EXERCICE 2 - RECHERCHE TABOUE")
print("=" * 55)

print("\nMeilleure solution trouvee :")
print("          M1   M2   M3   Total")
print("D1       ", x1, " ", sum(x1))
print("D2       ", x2, " ", sum(x2))
print("Total     4    5    8     17")

print("\nCout minimum :", meilleure_distance)
