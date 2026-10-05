# ==============================================================================
# PROJET : COMPTEUR DE JOURS ALGORITHMIQUE (INCLUSIF ET SÉCURISÉ)
# ==============================================================================

def est_bissextile(annee):
    """
    Vérifie si une année donnée est bissextile.
    Règle : Divisible par 4 ET non par 100, OU divisible par 400.
    """
    divisible_par_4 = (annee % 4 == 0)
    non_divisible_par_100 = (annee % 100 != 0)
    divisible_par_400 = (annee % 400 == 0)
    
    return (divisible_par_4 and non_divisible_par_100) or divisible_par_400


def jours_dans_mois(mois, annee):
    """
    Renvoie le nombre exact de jours pour un mois et une année donnés.
    """
    if mois in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif mois in [4, 6, 9, 11]:
        return 30
    elif mois == 2:
        return 29 if est_bissextile(annee) else 28
    
    return 0


def jour_de_lannee(jour, mois, annee):
    """
    Calcule le numéro du jour dans l'année (rang du jour).
    """
    total = 0
    for m in range(1, mois):
        total += jours_dans_mois(m, annee)
    total += jour
    return total


def calculer_jours(j1, m1, a1, j2, m2, a2):
    """
    Calcule le nombre total de jours entre deux dates, jour de départ inclus (+1).
    """
    if a1 == a2:
        rang_debut = jour_de_lannee(j1, m1, a1)
        rang_fin = jour_de_lannee(j2, m2, a2)
        return (rang_fin - rang_debut) + 1

    total_jours = 0
    
    # 1. Jours restants dans la première année
    nb_jours_a1 = 366 if est_bissextile(a1) else 365
    rang_debut = jour_de_lannee(j1, m1, a1)
    total_jours += (nb_jours_a1 - rang_debut) + 1
    
    # 2. Années complètes intermédiaires
    for annee in range(a1 + 1, a2):
        total_jours += 366 if est_bissextile(annee) else 365
        
    # 3. Jours écoulés dans la dernière année
    rang_fin = jour_de_lannee(j2, m2, a2)
    total_jours += rang_fin
    
    return total_jours


# ==============================================================================
# NOUVELLES FONCTIONS DE VALIDATION (AMÉLIORATION)
# ==============================================================================

def demander_date_valide(message_invite):
    """
    Demande une date à l'utilisateur et boucle tant que la saisie 
    n'est pas au bon format (JJ/MM/AAAA) ou que la date est physiquement impossible.
    """
    while True:
        saisie = input(message_invite).strip()
        
        # 1. Vérification de la présence des deux séparateurs '/'
        parties = saisie.split('/')
        if len(parties) != 3:
            print("Erreur : Le format doit être exactement JJ/MM/AAAA (ex: 15/03/2024). Réessayez.\n")
            continue
        
        # 2. Vérification que chaque partie est bien un nombre entier
        try:
            j = int(parties[0])
            m = int(parties[1])
            a = int(parties[2])
        except ValueError:
            print("Erreur : La date ne doit contenir que des chiffres et des '/'. Réessayez.\n")
            continue
            
        # 3. Vérification de la validité du mois (1 à 12)
        if m < 1 or m > 12:
            print(f"Erreur : Le mois ({m}) n'existe pas. Il doit être entre 1 et 12. Réessayez.\n")
            continue
            
        # 4. Vérification de la validité du jour par rapport au mois et à l'année
        max_jours = jours_dans_mois(m, a)
        if j < 1 or j > max_jours:
            print(f"Erreur : Le jour ({j}) est invalide pour le mois {m}/{a} (max {max_jours} jours). Réessayez.\n")
            continue
            
        # Si tout est valide, on renvoie les composants de la date et la chaîne
        return j, m, a, saisie


# ==============================================================================
# PROGRAMME PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    print("=== COMPTEUR DE JOURS ALGORITHMIQUE ===")
    
    # Boucle principale : tourne tant que l'ordre des dates est incorrect
    while True:
        print("\n--- Saisie des dates ---")
        d_j, d_m, d_a, d_str = demander_date_valide("Date de début (JJ/MM/AAAA) : ")
        f_j, f_m, f_a, f_str = demander_date_valide("Date de fin   (JJ/MM/AAAA) : ")

        # Vérification de l'ordre chronologique (année, puis mois, puis jour)
        date_debut_apres_fin = (d_a, d_m, d_j) > (f_a, f_m, f_j)
        
        if date_debut_apres_fin:
            print("\n Erreur : La date de début est plus récente que la date de fin !")
            print(" Veuillez recommencer la saisie depuis le début.")
        else:
            # Si l'ordre est correct, on sort de la boucle principale
            break

    # Calcul et affichage du résultat
    resultat = calculer_jours(d_j, d_m, d_a, f_j, f_m, f_a)
    print(f"\nRésultat : Il y a {resultat} jours du {d_str} au {f_str} (jour de départ inclus).")