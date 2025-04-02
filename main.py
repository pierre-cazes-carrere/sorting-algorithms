import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from sorting import heap_sort, comb_sort  # Assure-toi que ton fichier sorting_algorithms.py est dans le même dossier

def execute_sort():
    """ Exécute le tri choisi et affiche le résultat """
    try:
        n = int(entry_n.get())
        if n < 1 or n > 1000000:
            raise ValueError("Le nombre doit être entre 1 et 1 million.")
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return
    
    # Générer une liste de nombres aléatoires
    arr = [random.randint(1, 1000000) for _ in range(n)]
    
    algorithm = algo_choice.get()
    
    start_time = time.time()
    
    if algorithm == "Tri par tas":
        heap_sort(arr)
    else:
        comb_sort(arr)
    
    end_time = time.time()
    
    # Affichage des résultats
    result_label.config(text=f"Temps d'exécution: {end_time - start_time:.6f} secondes")
    sorted_list_label.config(text=f"Liste triée (10 premiers): {arr[:10]} ...")

def reset_fields():
    """ Réinitialise les champs d'entrée et de résultat """
    entry_n.set(1)
    result_label.config(text="")
    sorted_list_label.config(text="")

def update_slider_value(val):
    """ Met à jour la valeur du slider et l'affiche """
    value_label.config(text=f"Taille de la liste : {int(float(val))}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Tri de Nombres")
root.geometry("500x500")  # Agrandir la fenêtre pour plus de confort
root.config(bg="#D4E6F1")  # Couleur de fond douce et moderne

# Titre
ttk.Label(root, text="Tri de nombres aléatoires", font=("Helvetica", 18, "bold"), background="#D4E6F1", foreground="#2C3E50").pack(pady=20)

# Section pour choisir la taille de la liste avec un slider
slider_frame = ttk.Frame(root, padding=10)
slider_frame.pack(pady=20)

ttk.Label(slider_frame, text="Choisir la taille de la liste :", background="#D4E6F1", font=("Helvetica", 12)).grid(row=0, column=0, padx=10)

entry_n = tk.DoubleVar(value=1)
slider = ttk.Scale(slider_frame, from_=1, to=1000000, orient="horizontal", variable=entry_n, command=update_slider_value, length=400)
slider.grid(row=1, column=0, padx=10)

# Ajuster l'échelle pour une meilleure précision sans utiliser tickinterval ni resolution
# Utiliser un facteur multiplicatif
slider.config(from_=1, to=100000)

value_label = ttk.Label(slider_frame, text="Taille de la liste : 1", background="#D4E6F1", font=("Helvetica", 12))
value_label.grid(row=2, column=0, padx=10)

# Sélection de l'algorithme
ttk.Label(root, text="Choisir l'algorithme de tri :", background="#D4E6F1", font=("Helvetica", 12)).pack(pady=10)
algo_choice = ttk.Combobox(root, values=["Tri par tas", "Tri à peigne"], state="readonly", font=("Helvetica", 12))
algo_choice.pack(pady=5)
algo_choice.current(0)  # Sélectionne par défaut "Tri par tas"

# Boutons
button_frame = ttk.Frame(root, padding=10)
button_frame.pack(pady=20)

# Modification de la couleur du texte des boutons ici
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=6, relief="flat", background="#4CAF50", foreground="black")  # Texte noir
style.map("TButton", background=[("active", "#45a049")])

style.configure("Accent.TButton", font=("Helvetica", 12, "bold"), padding=6, relief="flat", background="#2196F3", foreground="white")  # Texte blanc
style.map("Accent.TButton", background=[("active", "#1976D2")])

sort_button = ttk.Button(button_frame, text="Lancer le tri", command=execute_sort, style="TButton", width=20)
sort_button.grid(row=0, column=0, padx=10)

reset_button = ttk.Button(button_frame, text="Réinitialiser", command=reset_fields, style="TButton", width=20)
reset_button.grid(row=0, column=1, padx=10)

# Affichage des résultats
result_label = ttk.Label(root, text="", font=("Helvetica", 12), background="#D4E6F1", foreground="#2C3E50")
result_label.pack(pady=10)

sorted_list_label = ttk.Label(root, text="", font=("Helvetica", 12), background="#D4E6F1", foreground="#2C3E50")
sorted_list_label.pack(pady=10)

# Lancement de l'interface
root.mainloop()
