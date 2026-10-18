import random
import math
from collections import deque


# ==========================================================
# TD n°2 - Exercice 3
# Voyageur de commerce
# 1) Recherche Taboue
# 2) Recuit Simule
# ==========================================================

# Matrice des distances du sujet.
# 0 = liaison absente.
# Le graphe est considere non oriente.

matrice_distances = [
    [0, 14, 15, 0, 0, 0, 0, 17],
    [14, 0, 13, 14, 20, 0, 0, 21],
    [15, 13, 0, 11, 21, 17, 9, 9],
    [0, 14, 11, 0, 11, 10, 8, 20],
    [0, 20, 21, 11, 0, 15, 18, 0],
    [0, 0, 17, 10, 15, 0, 9, 0],
    [0, 0, 9, 8, 18, 9, 0, 13],
    [17, 21, 9, 20, 0, 0, 13, 0]
]


def calculer_distance_totale(solution, matrice_distances):
    """
    Calcule la distance du circuit complet :
    solution[0] -> ... -> solution[-1] -> solution[0].
    """
    distance_totale = 0

    for i in range(len(solution) - 1):

        ville1 = solution[i] - 1
        ville2 = solution[i + 1] - 1

        if matrice_distances[ville1][ville2] == 0:
            return float("inf")

        distance_totale += matrice_distances[ville1][ville2]

    # Retour a la ville de depart
    ville1 = solution[-1] - 1
    ville2 = solution[0] - 1

    if matrice_distances[ville1][ville2] == 0:
        return float("inf")

    distance_totale += matrice_distances[ville1][ville2]

    return distance_totale


def generer_voisins(solution):
    """
    Genere les voisins par echange de deux villes.
    La ville 1 reste fixe.
    """
    voisins = []

    for i in range(1, len(solution)):
        for j in range(i + 1, len(solution)):

            voisin = solution[:]

            voisin[i], voisin[j] = voisin[j], voisin[i]

            voisins.append(voisin)

    return voisins


def tabou_search(matrice_distances, nombre_iterations, taille_tabou):
    """
    Recherche taboue avec la solution initiale imposee
    par l'enonce : 1-2-3-4-5-6-7-8.
    """
    solution_actuelle = [1, 2, 3, 4, 5, 6, 7, 8]

    meilleure_solution = solution_actuelle[:]

    meilleure_distance = calculer_distance_totale(
        solution_actuelle,
        matrice_distances
    )

    tabou_list = deque(maxlen=taille_tabou)

    for _ in range(nombre_iterations):

        voisins = generer_voisins(solution_actuelle)

        # Garder uniquement les circuits possibles
        voisins = [
            voisin for voisin in voisins
            if calculer_distance_totale(
                voisin, matrice_distances
            ) != float("inf")
        ]

        # Eviter les solutions presentes dans la liste taboue
        voisins = [
            voisin for voisin in voisins
            if voisin not in tabou_list
        ]

        if not voisins:
            break

        solution_actuelle = min(
            voisins,
            key=lambda x: calculer_distance_totale(
                x, matrice_distances
            )
        )

        distance_actuelle = calculer_distance_totale(
            solution_actuelle,
            matrice_distances
        )

        tabou_list.append(solution_actuelle[:])

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance


def recuit_simule(matrice_distances, nombre_iterations,
                  temperature_initiale, alpha):
    """
    Recuit simule :
    - 5 iterations
    - T0 = 20
    - T(k+1) = alpha * T(k)
    """
    solution_actuelle = [1, 2, 3, 4, 5, 6, 7, 8]

    meilleure_solution = solution_actuelle[:]

    distance_actuelle = calculer_distance_totale(
        solution_actuelle,
        matrice_distances
    )

    meilleure_distance = distance_actuelle

    temperature = temperature_initiale

    for iteration in range(nombre_iterations):

        voisins = generer_voisins(solution_actuelle)

        # On garde les circuits valides
        voisins = [
            voisin for voisin in voisins
            if calculer_distance_totale(
                voisin, matrice_distances
            ) != float("inf")
        ]

        if not voisins:
            break

        # Choix aleatoire d'un voisin
        voisin = random.choice(voisins)

        distance_voisin = calculer_distance_totale(
            voisin,
            matrice_distances
        )

        delta = distance_voisin - distance_actuelle

        accepte = False
        probabilite = 1.0

        if delta <= 0:
            accepte = True

        else:
            probabilite = math.exp(
                -delta / temperature
            )

            if random.random() < probabilite:
                accepte = True

        if accepte:
            solution_actuelle = voisin
            distance_actuelle = distance_voisin

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

        print(
            "Iteration", iteration + 1,
            "| T =", round(temperature, 6),
            "| voisin =", voisin,
            "| distance =", distance_voisin,
            "| delta =", delta,
            "| accepte =", accepte
        )

        # Refroidissement empirique
        temperature = temperature * alpha

    return meilleure_solution, meilleure_distance


def afficher_solution(solution, distance):
    circuit = solution + [solution[0]]

    print(
        "Solution :",
        " -> ".join(map(str, circuit))
    )

    print("Distance :", distance)


# ==========================================================
# Programme principal
# ==========================================================

print("=" * 60)
print("EXERCICE 3 - VOYAGEUR DE COMMERCE")
print("=" * 60)

solution_initiale = [1, 2, 3, 4, 5, 6, 7, 8]

print("\nSolution initiale :")
afficher_solution(
    solution_initiale,
    calculer_distance_totale(
        solution_initiale,
        matrice_distances
    )
)


# ----------------------------------------------------------
# 1. RECHERCHE TABOUE
# ----------------------------------------------------------

print("\n1. RECHERCHE TABOUE")
print("-------------------")

meilleure_solution, meilleure_distance = tabou_search(
    matrice_distances,
    nombre_iterations=100,
    taille_tabou=10
)
print("\nMeilleure solution trouvee :")
afficher_solution(
    meilleure_solution,
    meilleure_distance
)
# ----------------------------------------------------------
# 2. RECUIT SIMULE
# ----------------------------------------------------------

print("\n2. RECUIT SIMULE")
print("----------------")

random.seed(42)

meilleure_solution, meilleure_distance = recuit_simule(
    matrice_distances,
    nombre_iterations=5,
    temperature_initiale=20,
    alpha=0.75
)

print("\nMeilleure solution trouvee :")
afficher_solution(
    meilleure_solution,
    meilleure_distance
)
