
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import random
import time
import threading
from sorting import HeapSort, CombSort, QuickSort, MergeSort

class SortingAlgorithm:
    def sort(self, arr):
        raise NotImplementedError

    def visualize(self, arr, visualizer):
        raise NotImplementedError

class HeapSort(SortingAlgorithm):
    def sort(self, arr):
        HeapSort(arr)

    def visualize(self, arr, visualizer):
        n = len(arr)
        for i in range(n // 2, -1, -1):
            self.heapify(arr, n, i)
        for i in range(n - 1, 0, -1):
            if visualizer.stop:
                return
            arr[i], arr[0] = arr[0], arr[i]
            if i % (n // 50 + 1) == 0:
                visualizer.draw(arr, ["#FF69B4"] * len(arr))
                time.sleep(0.01)
            self.heapify(arr, i, 0)

    def heapify(self, arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)

class CombSort(SortingAlgorithm):
    def sort(self, arr):
         CombSort(arr)

    def visualize(self, arr, visualizer):
        gap, shrink = len(arr), 1.3
        while gap > 1:
            if visualizer.stop:
                return
            gap = max(1, int(gap / shrink))
            for i in range(len(arr) - gap):
                if arr[i] > arr[i + gap]:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
            visualizer.draw(arr, ["#FF69B4"] * len(arr))
            time.sleep(0.01)

class QuickSort(SortingAlgorithm):
    def sort(self, arr):
        arr[:] = QuickSort(arr)

class MergeSort(SortingAlgorithm):
    def sort(self, arr):
        arr[:] = MergeSort(arr)

class Visualizer:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.stop = False

    def draw(self, arr, colors):
        self.canvas.delete("all")
        c_width, c_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        bar_width = max(1, c_width / max(len(arr), 1))
        max_val = max(arr, default=1)
        for i, value in enumerate(arr):
            x0, y0 = i * bar_width, c_height - (value / max_val) * c_height
            x1, y1 = (i + 1) * bar_width, c_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline="black")
        self.root.update_idletasks()

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.visualizer = Visualizer(canvas, root)
        self.algorithms = {
            "Tri par tas": HeapSort(),
            "Tri à peigne": CombSort(),
            "Tri rapide": QuickSort(),
            "Tri fusion": MergeSort(),
        }
        self.setup_ui()

    def setup_ui(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.title("Tri de Nombres")
        self.root.geometry("800x600")
        self.root.config(bg="#FFC0CB")

        ctk.CTkLabel(self.root, text="Le Tri de Héron", font=("Helvetica", 20, "bold")).pack(fill="x")

        slider_frame = ctk.CTkFrame(self.root)
        slider_frame.pack(pady=10)
        self.slider = ctk.CTkSlider(slider_frame, from_=1, to=100000, command=self.update_slider_value, number_of_steps=5000)
        self.slider.pack()
        self.slider.set(1)
        self.value_label = ctk.CTkLabel(slider_frame, text="Taille de la liste : 1")
        self.value_label.pack()

        self.algo_choice = ctk.CTkComboBox(self.root, values=list(self.algorithms.keys()))
        self.algo_choice.pack()
        self.algo_choice.set("Tri par tas")

        self.entry_results = ctk.CTkEntry(self.root, width=10)
        self.entry_results.pack()
        self.entry_results.insert(0, "10")

        ctk.CTkButton(self.root, text="Lancer le tri", command=self.execute_sort).pack()
        ctk.CTkButton(self.root, text="Réinitialiser", command=self.reset_fields).pack()

        self.visualize_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self.root, text="Activer la visualisation", variable=self.visualize_var).pack()

        self.result_tree = ttk.Treeview(self.root, columns=("Index", "Valeur"), show="headings")
        self.result_tree.heading("Index", text="Index")
        self.result_tree.heading("Valeur", text="Valeur triée")
        self.result_tree.pack()

    def update_slider_value(self, val):
        self.value_label.configure(text=f"Taille de la liste : {int(float(val))}")

    def execute_sort(self):
        self.visualizer.stop = False
        try:
            n = int(self.slider.get())
            num_results = int(self.entry_results.get())
            if n < 1 or n > 100000 or num_results < 1 or num_results > n:
                raise ValueError("Taille invalide")
        except ValueError as e:
            ctk.CTkMessagebox(title="Erreur", message=str(e), icon="error")
            return

        arr = [random.randint(1, 1000000) for _ in range(n)]
        algo_name = self.algo_choice.get()
        algorithm = self.algorithms[algo_name]
        start_time = time.time()

        if self.visualize_var.get() and hasattr(algorithm, "visualize"):
            threading.Thread(target=self._visualize_sort, args=(arr, algorithm), daemon=True).start()
        else:
            algorithm.sort(arr)
            self.update_results(arr, time.time() - start_time, num_results)

    def _visualize_sort(self, arr, algorithm):
        self.visualizer.draw(arr, ["#FF69B4"] * len(arr))
        algorithm.visualize(arr, self.visualizer)
        self.visualizer.draw(arr, ["green"] * len(arr))

    def update_results(self, arr, execution_time, num_results):
        self.result_tree.delete(*self.result_tree.get_children())
        for i, value in enumerate(arr[:num_results]):
            self.result_tree.insert("", "end", values=(i + 1, value))
        ctk.CTkMessagebox(title="Tri terminé", message=f"Temps d'exécution: {execution_time:.6f} secondes", icon="info")

    def reset_fields(self):
        self.visualizer.stop = True
        self.entry_results.delete(0, tk.END)
        self.entry_results.insert(0, "10")
        self.result_tree.delete(*self.result_tree.get_children())
        self.slider.set(1)
        self.value_label.configure(text=f"Taille de la liste : 1")
        canvas.delete("all")

if __name__ == "__main__":
    root = ctk.CTk()
    canvas = tk.Canvas(root, bg="white")
    canvas.pack(fill="both", expand=True)
    app = SortingApp(root)
    root.mainloop()
