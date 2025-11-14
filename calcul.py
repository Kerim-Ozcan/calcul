import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ast
import os

# liste des coeficients dans des dictionaires pour chaque UE
coef_ue1 ={
    'R101':10, 'R102':10, 'R103':7, 'R104':7, 'R105': 0, 'R106':5,
    'R107': 0, 'R108':6, 'R109': 0, 'R110':5, 'R111':4, 'R112':2, 'R113':5,
    'R114':5, 'R115': 0, 'SAE11':20, 'SAE12':20, 'SAE16':7
}
coef_ue2 ={
    'R101': 4, 'R102': 0, 'R103':2, 'R104':8, 'R105':6, 'R106': 0, 
    'R107': 0, 'R108': 0, 'R109': 0, 'R110': 5, 'R111':5, 'R112':2, 'R113':9, 'R114':9, 
    'R115':5,'SAE13':29, 'SAE16':7
}
coef_ue3 ={
    'R101':4, 'R102': 0, 'R103':2, 'R104': 0, 'R105': 0,'R106':5, 'R107':15, 'R108':6,
    'R109':4, 'R110':5, 'R111':5, 'R112':2, 'R115':3,
    'SAE14':20, 'SAE15':20, 'SAE16':7
}

# Importation des notes depuis le fichier "notes"
notes_fichier = "notes.txt"
notes = {}
if os.path.exists(notes_fichier):
    try:
        with open(notes_fichier, "r", encoding="utf-8") as f:
            contenu = f.read()
            notes = ast.literal_eval(contenu)
    except Exception as e:
        print("Erreur lors du chargement du fichier de notes :", e)
else:
    print("Fichier notes.txt introuvable.")
    notes = {}

# fonction pour calculer la moyenne d'un UE
def calculer_moyenne_ue(coefs, notes):
    total_points=0
    total_coefs=0
    for matiere, coef in coefs.items():
        if matiere in notes:
            total_points +=notes[matiere] * coef
            total_coefs +=coef
    if total_coefs == 0:
        return 0
    return total_points / total_coefs

# fonction pour choisir la couleur des moyennes 
def get_color(value):
    if value>=10:
        return 'green'
    elif value>=8:
        return 'orange'
    else:
        return 'red'

# creation de la fenetre
fenetre=tk.Tk()
fenetre.geometry("400x300")
fenetre.title("Moyennes Automatiques")

frm=ttk.Frame(fenetre, padding=10)
frm.pack()

# calcul des moyenne par UE
moyenne_ue1=calculer_moyenne_ue(coef_ue1, notes)
moyenne_ue2=calculer_moyenne_ue(coef_ue2, notes)
moyenne_ue3=calculer_moyenne_ue(coef_ue3, notes)

values=[moyenne_ue1, moyenne_ue2, moyenne_ue3]
colors=[get_color(v) for v in values]

# creation du graphique 
plt.figure(figsize=(5, 3))
plt.bar(['UE1', 'UE2', 'UE3'], values, color=colors)
plt.ylim(0, 20)
plt.title("Moyennes par UE")
plt.ylabel("Moyenne")
plt.axhline(10, color='gray', linestyle='--')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("moyennes_ue.png")
plt.close()

# Affichage du graphique 
img=Image.open("moyennes_ue.png")
img=img.resize((320, 200))

photo=ImageTk.PhotoImage(img)
image_label=ttk.Label(frm, image=photo)
image_label.pack(pady=10)

fenetre.mainloop()
