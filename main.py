import tkinter as tk
from tkinter import ttk, messagebox

# ==============================================================================
# LOGIQUE ALGORITHMIQUE (Backend inchangé)
# ==============================================================================

def est_bissextile(annee):
    """Vérifie si une année donnée est bissextile."""
    divisible_par_4 = (annee % 4 == 0)
    non_divisible_par_100 = (annee % 100 != 0)
    divisible_par_400 = (annee % 400 == 0)
    return (divisible_par_4 and non_divisible_par_100) or divisible_par_400


def jours_dans_mois(mois, annee):
    """Renvoie le nombre exact de jours pour un mois et une année donnés."""
    if mois in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif mois in [4, 6, 9, 11]:
        return 30
    elif mois == 2:
        return 29 if est_bissextile(annee) else 28
    return 0


def jour_de_lannee(jour, mois, annee):
    """Calcule le numéro du jour dans l'année (rang du jour)."""
    total = 0
    for m in range(1, mois):
        total += jours_dans_mois(m, annee)
    total += jour
    return total


def calculer_jours(j1, m1, a1, j2, m2, a2):
    """Calcule le nombre total de jours entre deux dates (inclusif)."""
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


def valider_et_analyser_date(chaine_date):
    """Vérifie et analyse une date au format JJ/MM/AAAA."""
    parties = chaine_date.strip().split('/')
    if len(parties) != 3:
        raise ValueError("Le format doit être exactement JJ/MM/AAAA (ex: 15/03/2024).")
    
    try:
        j = int(parties[0])
        m = int(parties[1])
        a = int(parties[2])
    except ValueError:
        raise ValueError("La date ne doit contenir que des chiffres et des '/'.")
        
    if m < 1 or m > 12:
        raise ValueError(f"Le mois ({m}) est invalide (doit être entre 1 et 12).")
        
    max_jours = jours_dans_mois(m, a)
    if j < 1 or j > max_jours:
        raise ValueError(f"Le jour ({j}) est invalide pour le mois {m}/{a} (max {max_jours} jours).")
        
    return j, m, a


# ==============================================================================
# INTERFACE GRAPHIQUE PROFESSIONNELLE (TKINTER + TTK)
# ==============================================================================

class ApplicationCompteurJours(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Configuration de la fenêtre principale ---
        self.title("Calculateur d'Intervalle Temporel - Professional Edition")
        
        # Dimensions grandes pour écran d'ordinateur (1000x650)
        largeur = 1000
        hauteur = 650
        
        # Centrage sur l'écran
        ecran_largeur = self.winfo_screenwidth()
        ecran_hauteur = self.winfo_screenheight()
        position_top = int((ecran_hauteur - hauteur) / 2)
        position_right = int((ecran_largeur - largeur) / 2)
        
        self.geometry(f"{largeur}x{hauteur}+{position_right}+{position_top}")
        self.minsize(800, 550)

        # Couleurs de la charte graphique moderne
        self.BG_MAIN = "#0f172a"        # Bleu nuit sombre (Arrière-plan principal)
        self.BG_CARD = "#1e293b"        # Gris bleu (Carte centrale)
        self.ACCENT = "#4f46e5"         # Indigo vibrant (Boutons / Focus)
        self.ACCENT_HOVER = "#4338ca"   # Indigo foncé
        self.TEXT_COLOR = "#f8fafc"     # Blanc cassé
        self.TEXT_MUTED = "#94a3b8"     # Gris clair pour sous-titres
        self.RESULT_BG = "#064e3b"      # Vert émeraude sombre
        self.RESULT_BORDER = "#10b981"  # Vert émeraude vif

        self.configure(bg=self.BG_MAIN)

        # Style TTK
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self._creer_interface()

    def _creer_interface(self):
        # Conteneur principal avec padding généreux
        container = tk.Frame(self, bg=self.BG_MAIN)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        # --- EN-TÊTE ---
        header_frame = tk.Frame(container, bg=self.BG_MAIN)
        header_frame.pack(fill="x", pady=(0, 20))

        title = tk.Label(
            header_frame,
            text="Compteur de Jours Algorithmique",
            font=("Segoe UI", 24, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_MAIN
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header_frame,
            text="Calculez la durée exacte entre deux dates avec validation algorithmique intégrée.",
            font=("Segoe UI", 11),
            fg=self.TEXT_MUTED,
            bg=self.BG_MAIN
        )
        subtitle.pack(anchor="w", pady=(5, 0))

        # --- CARTE CENTRALE (Formulaire) ---
        card = tk.Frame(container, bg=self.BG_CARD, bd=1, relief="flat")
        card.pack(fill="x", pady=10, ipady=15, ipadx=15)

        # Configuration des colonnes pour un alignement réactif
        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)

        # Champ Date de Début
        frame_debut = tk.Frame(card, bg=self.BG_CARD)
        frame_debut.grid(row=0, column=0, sticky="ew", padx=20, pady=15)

        lbl_debut = tk.Label(
            frame_debut, 
            text="DATE DE DÉBUT", 
            font=("Segoe UI", 9, "bold"), 
            fg=self.TEXT_MUTED, 
            bg=self.BG_CARD
        )
        lbl_debut.pack(anchor="w", pady=(0, 5))

        self.entry_debut = tk.Entry(
            frame_debut,
            font=("Segoe UI", 14),
            bg="#334155",
            fg=self.TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            bd=8
        )
        self.entry_debut.pack(fill="x")
        self.entry_debut.insert(0, "01/01/2026")

        # Champ Date de Fin
        frame_fin = tk.Frame(card, bg=self.BG_CARD)
        frame_fin.grid(row=0, column=1, sticky="ew", padx=20, pady=15)

        lbl_fin = tk.Label(
            frame_fin, 
            text="DATE DE FIN", 
            font=("Segoe UI", 9, "bold"), 
            fg=self.TEXT_MUTED, 
            bg=self.BG_CARD
        )
        lbl_fin.pack(anchor="w", pady=(0, 5))

        self.entry_fin = tk.Entry(
            frame_fin,
            font=("Segoe UI", 14),
            bg="#334155",
            fg=self.TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            bd=8
        )
        self.entry_fin.pack(fill="x")
        self.entry_fin.insert(0, "31/12/2026")

        # --- BOUTON D'ACTION ---
        btn_frame = tk.Frame(container, bg=self.BG_MAIN)
        btn_frame.pack(fill="x", pady=20)

        self.btn_calculer = tk.Button(
            btn_frame,
            text="CALCULER L'INTERVALLE",
            font=("Segoe UI", 12, "bold"),
            bg=self.ACCENT,
            fg="white",
            activebackground=self.ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=12,
            command=self.action_calculer
        )
        self.btn_calculer.pack(fill="x")

        # --- ZONE DE RÉSULTAT (Style Carte d'Information) ---
        self.result_card = tk.Frame(container, bg=self.BG_CARD, bd=1, relief="flat")
        self.result_card.pack(fill="both", expand=True, pady=(10, 0))

        self.lbl_resultat_titre = tk.Label(
            self.result_card,
            text="RÉSULTAT DU CALCUL",
            font=("Segoe UI", 9, "bold"),
            fg=self.TEXT_MUTED,
            bg=self.BG_CARD
        )
        self.lbl_resultat_titre.pack(anchor="w", padx=25, pady=(20, 5))

        self.lbl_resultat_valeur = tk.Label(
            self.result_card,
            text="Saisissez vos dates puis cliquez sur le bouton ci-dessus.",
            font=("Segoe UI", 15),
            fg=self.TEXT_COLOR,
            bg=self.BG_CARD,
            wraplength=850,
            justify="left"
        )
        self.lbl_resultat_valeur.pack(anchor="w", padx=25, pady=(0, 20))

    def action_calculer(self):
        saisie_debut = self.entry_debut.get()
        saisie_fin = self.entry_fin.get()

        # 1. Validation de la date de début
        try:
            d_j, d_m, d_a = valider_et_analyser_date(saisie_debut)
        except ValueError as e:
            messagebox.showerror("Erreur - Date de début", str(e))
            return

        # 2. Validation de la date de fin
        try:
            f_j, f_m, f_a = valider_et_analyser_date(saisie_fin)
        except ValueError as e:
            messagebox.showerror("Erreur - Date de fin", str(e))
            return

        # 3. Vérification de l'ordre chronologique
        if (d_a, d_m, d_j) > (f_a, f_m, f_j):
            messagebox.showerror(
                "Ordre Chronologique Incorrect",
                "La date de début est plus récente que la date de fin !\n\nVeuillez vérifier vos dates."
            )
            return

        # 4. Calcul et affichage
        total = calculer_jours(d_j, d_m, d_a, f_j, f_m, f_a)
        
        # Mise à jour visuelle du bloc de résultat
        self.result_card.configure(bg=self.RESULT_BG)
        self.lbl_resultat_titre.configure(bg=self.RESULT_BG, fg="#a7f3d0")
        self.lbl_resultat_valeur.configure(
            bg=self.RESULT_BG,
            fg="#ffffff",
            font=("Segoe UI", 18, "bold"),
            text=f"Il y a {total:,} jours entre le {saisie_debut} et le {saisie_fin}.\n(Jour de départ inclus)".replace(",", " ")
        )


if __name__ == "__main__":
    app = ApplicationCompteurJours()
    app.mainloop()