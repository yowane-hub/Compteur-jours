# ==============================================================================
# PROJET : COMPTEUR DE JOURS ALGORITHMIQUE (INCLUSIF)
# ==============================================================================

def est_bissextile(annee):
    """
    Vérifie si une année donnée est bissextile.
    Règle : Divisible par 4 ET non par 100, OU divisible par 400.
    """
    divisible_par_4 = (annee % 4 == 0)
    non_divisible_par_100 = (annee % 100 != 0)
    divisible_par_400 = (annee % 400 == 0)
    
    # Renvoie True si l'année compte 366 jours, sinon False
    return (divisible_par_4 and non_divisible_par_100) or divisible_par_400


def jours_dans_mois(mois, annee):
    """
    Renvoie le nombre exact de jours pour un mois et une année donnés.
    """
    # Mois à 31 jours
    if mois in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    # Mois à 30 jours
    elif mois in [4, 6, 9, 11]:
        return 30
    # Cas de Février (28 ou 29 jours selon l'année)
    elif mois == 2:
        return 29 if est_bissextile(annee) else 28
    
    return 0


def jour_de_lannee(jour, mois, annee):
    """
    Calcule le numéro du jour dans l'année (rang du jour).
    Exemple : 15 Février 2024 -> 31 (Janvier) + 15 = 46e jour.
    """
    total = 0
    # On additionne les jours de tous les mois précédant le mois actuel
    for m in range(1, mois):
        total += jours_dans_mois(m, annee)
    
    # On ajoute les jours du mois en cours
    total += jour
    return total


def calculer_jours(j1, m1, a1, j2, m2, a2):
    """
    Calcule le nombre total de jours entre deux dates, jour de départ inclus (+1).
    """
    # --------------------------------------------------------------------------
    # CAS 1 : Les deux dates sont dans la même année
    # --------------------------------------------------------------------------
    if a1 == a2:
        rang_debut = jour_de_lannee(j1, m1, a1)
        rang_fin = jour_de_lannee(j2, m2, a2)
        # Formule inclusives dans la même année
        return (rang_fin - rang_debut) + 1

    # --------------------------------------------------------------------------
    # CAS 2 : Les dates sont sur des années différentes
    # --------------------------------------------------------------------------
    total_jours = 0
    
    # 1. Jours restants dans la première année (a1)
    nb_jours_a1 = 366 if est_bissextile(a1) else 365
    rang_debut = jour_de_lannee(j1, m1, a1)
    total_jours += (nb_jours_a1 - rang_debut) + 1  # +1 pour inclure le jour de départ
    
    # 2. Années complètes intermédiaires (strictement entre a1 et a2)
    for annee in range(a1 + 1, a2):
        total_jours += 366 if est_bissextile(annee) else 365
        
    # 3. Jours écoulés dans la dernière année (a2)
    rang_fin = jour_de_lannee(j2, m2, a2)
    total_jours += rang_fin
    
    return total_jours


# ==============================================================================
# PROGRAMME PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    print("=== COMPTEUR DE JOURS ALGORITHMIQUE ===")
    
    # Saisie des dates au format JJ/MM/AAAA
    d_str = input("Date de début (JJ/MM/AAAA) : ")
    d_j, d_m, d_a = map(int, d_str.split('/'))

    f_str = input("Date de fin (JJ/MM/AAAA)   : ")
    f_j, f_m, f_a = map(int, f_str.split('/'))

    # Calcul du résultat
    resultat = calculer_jours(d_j, d_m, d_a, f_j, f_m, f_a)

    # Affichage final
    print(f"\nRésultat : Il y a {resultat} jours du {d_str} au {f_str} (jour de départ inclus).")