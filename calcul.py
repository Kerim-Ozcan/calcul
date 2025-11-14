# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Coefficients des matières pour chaque UE
coef_ue1 = {
    'R101':10, 'R102':10, 'R103':7, 'R104':7, 'R105': 0, 'R106':5,
    'R107': 0, 'R108':6, 'R109': 0, 'R110':5, 'R111':4, 'R112':2, 'R113':5,
    'R114':5, 'R115': 0, 'SAE11':20, 'SAE16':7
}
coef_ue2 = {
    'R101': 4, 'R102': 0, 'R103':2, 'R104':8, 'R105':6, 'R106': 0, 
    'R107': 0, 'R108': 0, 'R109': 0, 'R110': 5, 'R111':5, 'R112':2, 'R113':9, 'R114':9, 
    'R115':5,'SAE13':29, 'SAE16':7
}
coef_ue3 = {
    'R101':4, 'R102': 0, 'R103':2, 'R104': 0, 'R105': 0,'R106':5, 'R107':15, 'R108':6,
    'R109':4, 'R110':5, 'R111':5, 'R112':2, 'R115':3,
    'SAE14':20, 'SAE15':20, 'SAE16':7
}

# Liste de toutes les matières (triée)
all_matieres = sorted(set(coef_ue1) | set(coef_ue2) | set(coef_ue3))

fenetre = tk.Tk()
fenetre.geometry("400x700")  # fenêtre plus petite, simple
fenetre.title("Calcul des moyennes")

frm = ttk.Frame(fenetre, padding=10)
frm.grid()

# Dictionnaire pour stocker les champs de saisie
entry_fields = {}

# Création des labels et champs pour chaque matière
for i, matiere in enumerate(all_matieres):
    ttk.Label(frm, text=matiere).grid(column=0, row=i, sticky='w', pady=2)
    entry = ttk.Entry(frm, width=10)
    entry.grid(column=1, row=i, pady=2)
    entry_fields[matiere] = entry

# Fonction pour calculer la moyenne pondérée d'une UE
def calculer_moyenne_ue(coefs, notes):
    total_points = 0
    total_coefs = 0
    for matiere, coef in coefs.items():
        if matiere in notes:
            total_points += notes[matiere] * coef
            total_coefs += coef
    if total_coefs == 0:
        return 0
    return total_points / total_coefs

# Fonction pour choisir la couleur en fonction de la note
def get_color(value):
    if value >= 10:
        return 'green'
    elif value >= 8:
        return 'orange'
    else:
        return 'red'

def valider():
    notes = {}
    erreurs = []

    # Lecture des notes entrées par l'utilisateur
    for matiere, entry in entry_fields.items():
        val = entry.get().strip()
        if val == '':
            continue  # on ignore les matières non remplies
        try:
            note = float(val.replace(',', '.'))  # accepte aussi la virgule
            if 0 <= note <= 20:
                notes[matiere] = note
            else:
                erreurs.append(f"{matiere}: note doit être entre 0 et 20")
        except ValueError:
            erreurs.append(f"{matiere}: entrée invalide")

    if erreurs:
        error_label.config(text="\n".join(erreurs))
        return
    else:
        error_label.config(text="")

    # Calcul des moyennes
    moyenne_ue1 = calculer_moyenne_ue(coef_ue1, notes)
    moyenne_ue2 = calculer_moyenne_ue(coef_ue2, notes)
    moyenne_ue3 = calculer_moyenne_ue(coef_ue3, notes)

    values = [moyenne_ue1, moyenne_ue2, moyenne_ue3]
    colors = [get_color(v) for v in values]

    # Création du graphique avec matplotlib
    plt.figure(figsize=(5,3))
    plt.bar(['UE1', 'UE2', 'UE3'], values, color=colors)
    plt.ylim(0, 20)
    plt.title("Moyennes par UE")
    plt.ylabel("Moyenne")
    plt.axhline(10, color='gray', linestyle='--')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("moyennes_ue.png")
    plt.close()

    # Chargement et affichage de l'image dans tkinter
    img = Image.open("moyennes_ue.png")
    img = img.resize((320, 200))  # taille plus raisonnable

    global photo  # il faut garder la référence sinon l'image disparait
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)

# Bouton pour lancer le calcul
btn_valider = ttk.Button(frm, text="Calculer Moyennes", command=valider)
btn_valider.grid(column=0, row=len(all_matieres)+1, columnspan=2, pady=10)

# Label pour afficher les erreurs
error_label = ttk.Label(frm, text="", foreground="red")
error_label.grid(column=0, row=len(all_matieres)+2, columnspan=2)

# Label pour afficher l'image matplotlib
image_label = ttk.Label(frm)
image_label.grid(column=0, row=len(all_matieres)+3, columnspan=2, pady=10)

fenetre.mainloop()
