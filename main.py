import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
from sorting import heap_sort, comb_sort

def execute_sort():
    try:
        n = int(entry_n.get())
        if n < 1 or n > 1000000:
            raise ValueError("Le nombre doit être entre 1 et 1 million.")
        
        num_results = int(entry_results.get())
        if num_results < 1 or num_results > n:
            raise ValueError("Le nombre de résultats doit être entre 1 et la taille de la liste.")

    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return

    arr = [random.randint(1, 1000000) for _ in range(n)]
    algorithm = algo_choice.get()
    start_time = time.time()

    if visualize_var.get():
        visualize_sort(arr, algorithm)  # Si la case est cochée, on affiche l'animation
    else:
        if algorithm == "Tri par tas":
            heap_sort(arr)
        else:
            comb_sort(arr)
        end_time = time.time()
        update_results(arr, end_time - start_time, num_results)

def update_results(arr, execution_time, num_results):
    result_tree.delete(*result_tree.get_children())

    for i, value in enumerate(arr[:num_results]):  
        result_tree.insert("", "end", values=(i+1, value))

    messagebox.showinfo("Tri terminé", f"Temps d'exécution: {execution_time:.6f} secondes")

def reset_fields():
    entry_n.set(1)
    entry_results.delete(0, tk.END)
    entry_results.insert(0, "10")
    result_tree.delete(*result_tree.get_children())
    slider.set(1)
    value_label.config(text="Taille de la liste : 1")
    canvas.delete("all")  # Effacer la visualisation si activée

def update_slider_value(val):
    value_label.config(text=f"Taille de la liste : {int(float(val))}")

def visualize_sort(arr, algorithm):
    canvas.delete("all")
    draw_bars(arr, ["blue"] * len(arr))

    def sorting_thread():
        if algorithm == "Tri par tas":
            heap_sort_with_visualization(arr)
        else:
            comb_sort_with_visualization(arr)

    threading.Thread(target=sorting_thread, daemon=True).start()

def draw_bars(arr, colors):
    canvas.delete("all")
    c_width = 600
    c_height = 200
    bar_width = c_width / len(arr)
    max_val = max(arr) if arr else 1

    # S'assurer que les barres ne sortent pas du canvas
    for i, value in enumerate(arr):
        x0 = i * bar_width
        y0 = c_height - (value / max_val) * c_height
        x1 = (i + 1) * bar_width
        y1 = c_height
        
        # Dessiner les barres avec un contour pour mieux visualiser
        canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline="black")

    root.update_idletasks()

def heap_sort_with_visualization(arr):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            draw_bars(arr, ["blue"] * len(arr))  # Dessiner les barres à chaque échange
            root.after(50)  # Attendre avant de continuer
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        draw_bars(arr, ["blue"] * len(arr))
        root.after(50)  # Attendre avant de continuer
        heapify(arr, i, 0)

def comb_sort_with_visualization(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                draw_bars(arr, ["blue"] * len(arr))  # Dessiner les barres à chaque échange
                root.after(50)  # Attendre avant de continuer

root = tk.Tk()
root.title("Tri de Nombres - Interface Rose")
root.geometry("700x700")
root.config(bg="#FFC0CB")

title_label = tk.Label(root, text="Le Tri de Héron", font=("Helvetica", 20, "bold"), bg="#FF69B4", fg="white", padx=20, pady=10)
title_label.pack(fill="x")

slider_frame = tk.Frame(root, bg="#FFC0CB")
slider_frame.pack(pady=10)

tk.Label(slider_frame, text="Taille de la liste :", bg="#FFC0CB", font=("Helvetica", 12)).grid(row=0, column=0, padx=10)

entry_n = tk.DoubleVar(value=1)
slider = ttk.Scale(slider_frame, from_=1, to=100000, orient="horizontal", variable=entry_n, command=update_slider_value, length=400)
slider.grid(row=1, column=0, padx=10)

value_label = tk.Label(slider_frame, text="Taille de la liste : 1", bg="#FFC0CB", font=("Helvetica", 12))
value_label.grid(row=2, column=0, padx=10)

tk.Label(root, text="Choisir l'algorithme :", bg="#FFC0CB", font=("Helvetica", 12)).pack(pady=10)
algo_choice = ttk.Combobox(root, values=["Tri par tas", "Tri à peigne"], state="readonly", font=("Helvetica", 12))
algo_choice.pack(pady=5)
algo_choice.current(0)

results_frame = tk.Frame(root, bg="#FFC0CB")
results_frame.pack(pady=10)

tk.Label(results_frame, text="Nombre de résultats à afficher :", bg="#FFC0CB", font=("Helvetica", 12)).grid(row=0, column=0, padx=10)

entry_results = tk.Entry(results_frame, font=("Helvetica", 12), width=5)
entry_results.grid(row=0, column=1, padx=5)
entry_results.insert(0, "10")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=6, relief="flat")
style.map("TButton", background=[("active", "#FF1493")], foreground=[("active", "white")])

button_frame = tk.Frame(root, bg="#FFC0CB")
button_frame.pack(pady=10)

sort_button = ttk.Button(button_frame, text="Lancer le tri", command=execute_sort, style="TButton", width=20)
sort_button.grid(row=0, column=0, padx=10)

reset_button = ttk.Button(button_frame, text="Réinitialiser", command=reset_fields, style="TButton", width=20)
reset_button.grid(row=0, column=1, padx=10)

# ✅ Ajout de la case à cocher pour afficher la visualisation
visualize_var = tk.BooleanVar(value=False)
visualize_checkbox = tk.Checkbutton(root, text="Activer la visualisation", variable=visualize_var, bg="#FFC0CB", font=("Helvetica", 12))
visualize_checkbox.pack(pady=5)

result_frame = tk.Frame(root, bg="#FFC0CB")
result_frame.pack(pady=10, fill="both", expand=True)

columns = ("Index", "Valeur")
result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=12, selectmode="none")

result_tree.heading("Index", text="Index", anchor="center")
result_tree.heading("Valeur", text="Valeur triée", anchor="center")
result_tree.column("Index", width=80, anchor="center")
result_tree.column("Valeur", width=200, anchor="center")

style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#FF69B4", foreground="white")

scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_tree.yview)
result_tree.configure(yscrollcommand=scrollbar.set)

result_tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(root, width=600, height=200, bg="white")
canvas.pack(pady=10)

root.mainloop()
