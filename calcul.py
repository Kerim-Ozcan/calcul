# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

coef_ue1 = {
    'R101':10, 'R102':10, 'R103':7, 'R104':7, 'R105': 0, 'R106':5,
    'R107': 0, 'R108':6, 'R109': 0, 'R110':5, 'R111':4, 'R112':2, 'R113':5,
    'R114':5, 'R115': 0, 'SAE11':20, 'SAE16':7
}
coef_ue2 = {
    'R101': 4, 'R102': 0, 'R103':2, 'R104':8, 'R105':6, 'R106': 0, 
    'R107': 0, 'R108': 0, 'R109': 0, 'R110': 5, 'R111':5, 'R112':2,
    'R113':9, 'R114':9, 'R115':5,'SAE13':29, 'SAE16':7
}
coef_ue3 = {
    'R101':4, 'R102': 0, 'R103':2, 'R104': 0, 'R105': 0,'R106':5,
    'R107':15, 'R108':6, 'R109':4, 'R110':5, 'R111':5, 'R112':2,
    'R115':3, 'SAE14':20, 'SAE15':20, 'SAE16':7
}

all_matieres = sorted(set(coef_ue1) | set(coef_ue2) | set(coef_ue3))

fenetre = tk.Tk()
fenetre.geometry("400x800")
fenetre.title("Outil de calcul des moyennes")

frm = ttk.Frame(fenetre, padding=10)
frm.grid()

entry_fields = {}

for i, matiere in enumerate(all_matieres):
    ttk.Label(frm, text=matiere).grid(column=0, row=i, pady=2)
    entry = ttk.Entry(frm, width=10)
    entry.grid(column=1, row=i, pady=2)
    entry_fields[matiere] = entry


def calculer_moyenne_ue(coefs, notes):
    total_points = 0
    total_coefs = 0
    for matiere, coef in coefs.items():
        if matiere in notes:
            total_points += notes[matiere] * coef
            total_coefs += coef
    return total_points / total_coefs if total_coefs > 0 else 0


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

    # Lecture des champs
    for matiere, entry in entry_fields.items():
        val = entry.get().strip()
        if val == "":
            continue
        try:
            note = float(val.replace(',', '.'))
            if 0 <= note <= 20:
                notes[matiere] = note
            else:
                erreurs.append(f"{matiere}: note invalide")
        except ValueError:
            erreurs.append(f"{matiere}: entrée non valide")

    # Affichage des erreurs
    if erreurs:
        error_label.config(text="\n".join(erreurs))
        return
    else:
        error_label.config(text="")

    # Calcul des moyennes
    moyenne_ue1 = calculer_moyenne_ue(coef_ue1, notes)
    moyenne_ue2 = calculer_moyenne_ue(coef_ue2, notes)
    moyenne_ue3 = calculer_moyenne_ue(coef_ue3, notes)

    print(f"Moyenne UE1 : {moyenne_ue1:.2f}")
    print(f"Moyenne UE2 : {moyenne_ue2:.2f}")
    print(f"Moyenne UE3 : {moyenne_ue3:.2f}")

    # Affichage graphique
    values = [moyenne_ue1, moyenne_ue2, moyenne_ue3]
    colors = [get_color(val) for val in values]

    plt.figure(figsize=(6,4))
    plt.bar(['UE1', 'UE2', 'UE3'], values, color=colors)
    plt.ylim(0, 20)
    plt.title("Moyennes par UE")
    plt.ylabel("Moyenne")
    plt.axhline(10, color='gray', linestyle='--', linewidth=1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()  # Pour afficher la fenêtre graphique


btn_valider = ttk.Button(frm, text="Calculer Moyennes", command=valider)
btn_valider.grid(column=0, row=len(all_matieres)+1, columnspan=2, pady=10)

error_label = ttk.Label(frm, text="", foreground='red')
error_label.grid(column=0, row=len(all_matieres)+2, columnspan=2)

fenetre.mainloop()


