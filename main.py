import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import random
import time
import threading
from sorting import heap_sort, comb_sort

stop_visualization = False

def execute_sort():
    global stop_visualization
    stop_visualization = False
    try:
        n = int(slider.get())
        if n < 1 or n > 100000:
            raise ValueError("Le nombre doit être entre 1 et 100 000.")
        num_results = int(entry_results.get())
        if num_results < 1 or num_results > n:
            raise ValueError("Le nombre de résultats doit être entre 1 et la taille de la liste.")
    except ValueError as e:
        ctk.CTkMessagebox(title="Erreur", message=str(e), icon="error")
        return
    
    arr = [random.randint(1, 1000000) for _ in range(n)]
    algorithm = algo_choice.get()
    start_time = time.time()
    
    if visualize_var.get():
        threading.Thread(target=visualize_sort, args=(arr, algorithm), daemon=True).start()
    else:
        if algorithm == "Tri par tas":
            heap_sort(arr)
        else:
            comb_sort(arr)
        update_results(arr, time.time() - start_time, num_results)

def update_results(arr, execution_time, num_results):
    result_tree.delete(*result_tree.get_children())
    for i, value in enumerate(arr[:num_results]):  
        result_tree.insert("", "end", values=(i+1, value))
    ctk.CTkMessagebox(title="Tri terminé", message=f"Temps d'exécution: {execution_time:.6f} secondes", icon="info")

def reset_fields():
    global stop_visualization
    stop_visualization = True
    entry_results.delete(0, tk.END)
    entry_results.insert(0, "10")
    result_tree.delete(*result_tree.get_children())
    slider.set(1)
    value_label.configure(text=f"Taille de la liste : 1")
    canvas.delete("all")

def update_slider_value(val):
    value_label.configure(text=f"Taille de la liste : {int(float(val))}")

def visualize_sort(arr, algorithm):
    global stop_visualization
    stop_visualization = False
    canvas.delete("all")
    draw_bars(arr, ["#FF69B4"] * len(arr))  # Rose
    
    if algorithm == "Tri par tas":
        heap_sort_with_visualization(arr)
    else:
        comb_sort_with_visualization(arr)
    
    draw_bars(arr, ["green"] * len(arr))

def draw_bars(arr, colors):
    canvas.delete("all")
    c_width, c_height = canvas.winfo_width(), canvas.winfo_height()
    bar_width = max(1, c_width / max(len(arr), 1))
    max_val = max(arr, default=1)
    
    for i, value in enumerate(arr):
        x0, y0 = i * bar_width, c_height - (value / max_val) * c_height
        x1, y1 = (i + 1) * bar_width, c_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline="black")
    root.update_idletasks()

def heap_sort_with_visualization(arr):
    global stop_visualization
    n = len(arr)
    for i in range(n // 2, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        if stop_visualization:
            return
        arr[i], arr[0] = arr[0], arr[i]
        if i % (n // 50 + 1) == 0:
            draw_bars(arr, ["#FF69B4"] * len(arr))  # Rose
            time.sleep(0.01)
        heapify(arr, i, 0)

def heapify(arr, n, i):
    largest, left, right = i, 2 * i + 1, 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def comb_sort_with_visualization(arr):
    global stop_visualization
    gap, shrink = len(arr), 1.3
    while gap > 1:
        gap = max(1, int(gap / shrink))
        for i in range(len(arr) - gap):
            if stop_visualization:
                return
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
        draw_bars(arr, ["#FF69B4"] * len(arr))  # Rose
        time.sleep(0.01)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Tri de Nombres")
root.geometry("800x600")
root.config(bg="#FFC0CB")

title_label = ctk.CTkLabel(root, text="Le Tri de Héron", font=("Helvetica", 20, "bold"))
title_label.pack(fill="x")

slider_frame = ctk.CTkFrame(root)
slider_frame.pack(pady=10)
slider = ctk.CTkSlider(slider_frame, from_=1, to=100000, command=update_slider_value, number_of_steps=5000)
slider.pack()
slider.set(1)  # Initialisation du curseur au début
value_label = ctk.CTkLabel(slider_frame, text="Taille de la liste : 1")
value_label.pack()

algo_choice = ctk.CTkComboBox(root, values=["Tri par tas", "Tri à peigne"])
algo_choice.pack()
algo_choice.set("Tri par tas")

entry_results = ctk.CTkEntry(root, width=10)
entry_results.pack()
entry_results.insert(0, "10")

sort_button = ctk.CTkButton(root, text="Lancer le tri", command=execute_sort)
sort_button.pack()

reset_button = ctk.CTkButton(root, text="Réinitialiser", command=reset_fields)
reset_button.pack()

visualize_var = ctk.BooleanVar(value=False)
visualize_checkbox = ctk.CTkCheckBox(root, text="Activer la visualisation", variable=visualize_var)
visualize_checkbox.pack()

result_tree = ttk.Treeview(root, columns=("Index", "Valeur"), show="headings")
result_tree.heading("Index", text="Index")
result_tree.heading("Valeur", text="Valeur triée")
result_tree.pack()

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)
root.mainloop()
