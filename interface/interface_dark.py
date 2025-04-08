import customtkinter as ctk
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import threading
import time
from tkinter import filedialog, ttk
import csv
from sorting.sorting import HeapSort, CombSort, QuickSort, MergeSort, SelectionSort, BubbleSort, InsertionSort, SortingAlgorithm





class SortingAppWithSeaborn:
    def __init__(self, root):
        self.animation_speed = 0.02
        self.root = root
        self.root.title("sorting algorithms")
        self.root.geometry("1000x700")
        CYBER_BG = "#2b2b2b"  # Define a default background color
        self.CYBER_TEXT = "#ffffff"  # Define a default text color
        self.root.configure(bg=CYBER_BG)
        ctk.set_appearance_mode("dark")

        self.algorithms = {
            "Tri par tas": HeapSort(),
            "Tri par sélection": SelectionSort(),
            "Tri à bulle": BubbleSort(),
            "Tri par insertion": InsertionSort(),
            "Tri à peigne": CombSort(),
            "Tri rapide": QuickSort(),
            "Tri fusion": MergeSort(),
            "Tri par sélection": SelectionSort(),
            "Tri à bulle": BubbleSort(),
            "Tri par insertion": InsertionSort()
        }

        self._setup_ui()

    
    def _update_speed(self, value):
        self.animation_speed = float(value)


    def _setup_ui(self):
        self.title_label = ctk.CTkLabel(self.root, text="Visualisation de Tri", font=("Consolas", 26, "bold"))
        self.title_label.pack(pady=10)

        self.slider = ctk.CTkSlider(self.root, from_=10, to=300, number_of_steps=290, command=self._update_slider_label)
        self.slider.set(50)
        self.slider.pack()
        self.slider_label = ctk.CTkLabel(self.root, text="Taille de la liste : 50")
        self.slider_label.pack()

        self.algo_choice = ctk.CTkComboBox(self.root, values=list(self.algorithms.keys()))
        self.algo_choice.pack(pady=10)
        self.algo_choice.set("Tri par tas")

        self.run_button = ctk.CTkButton(self.root, text="Démarrer", command=self._start_sorting)
        self.run_button.pack(pady=5)

        self.competition_button = ctk.CTkButton(self.root, text="Mode Compétition", command=self._open_competition)
        self.competition_button.pack(pady=10)

        self.canvas_frame = ctk.CTkFrame(self.root)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.speed_slider = ctk.CTkSlider(self.root, from_=0.001, to=0.1, number_of_steps=100, command=self._update_speed)
        self.speed_slider.set(0.02)
        self.speed_slider.pack(pady=5)
        self.speed_label = ctk.CTkLabel(self.root, text="Vitesse de l'animation")
        self.speed_label.pack()


        self.before_label = ctk.CTkLabel(self.root, text="Avant tri : []", text_color=self.CYBER_TEXT)
        self.before_label.pack(pady=5)

        self.after_label = ctk.CTkLabel(self.root, text="Après tri : []", text_color=self.CYBER_TEXT)
        self.after_label.pack(pady=5)


    def _update_slider_label(self, val):
        self.slider_label.configure(text=f"Taille de la liste : {int(float(val))}")

    def _start_sorting(self):
        threading.Thread(target=self._run_sorting, daemon=True).start()

    def _run_sorting(self):
        n = int(self.slider.get())
        data = [random.randint(1, 100) for _ in range(n)]
        algo_name = self.algo_choice.get()
        algorithm = self.algorithms[algo_name]
        self.before_label.configure(text="Avant tri : " + str(data))
        self._animate_sort(data, algorithm)
        self.after_label.configure(text="Après tri : " + str(data))

    def _animate_sort(self, data, algorithm):
        def update_plot(data, color="skyblue"):
            self.ax.clear()
            sns.barplot(x=list(range(len(data))), y=data, ax=self.ax, palette="coolwarm")
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.canvas.draw()
            self.root.update()

        if isinstance(algorithm, QuickSort):
            self._quick_sort_anim(data, update_plot)
        elif isinstance(algorithm, MergeSort):
            self._merge_sort_anim(data, update_plot)
        else:
            class AnimatedAlgo(algorithm.__class__):
                def sort(self_inner, arr):
                    self_inner.draw_step = self.draw_step
                    super(self_inner.__class__, self_inner).sort(arr)
            animated_algo = AnimatedAlgo()
            animated_algo.sort(data)
            update_plot(data, "green")

    def draw_step(self, arr, color_positions=None):
        if color_positions is None:
            color_positions = {}

        self.ax.clear()
        palette = []
        for i in range(len(arr)):
            if i in color_positions.get("compare", []):
                palette.append("#FFD700")  # jaune
            elif i in color_positions.get("swap", []):
                palette.append("#FF4C4C")  # rouge
            elif i in color_positions.get("sorted", []):
                palette.append("#00FF99")  # vert fluo
            else:
                palette.append("#00FFFF")  # couleur de base

        sns.barplot(x=list(range(len(arr))), y=arr, ax=self.ax, palette=palette)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title("Tri à bulles - Animation optimisée", fontsize=14)
        self.canvas.draw()
        self.root.update()
        time.sleep(self.animation_speed)

    def _quick_sort_anim(self, arr, draw_callback):
        def quick_sort_recursive(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_recursive(arr, low, pi - 1)
                quick_sort_recursive(arr, pi + 1, high)

        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    draw_callback(arr)
                    time.sleep(self.animation_speed)
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            draw_callback(arr)
            time.sleep(self.animation_speed)
            return i + 1

        quick_sort_recursive(arr, 0, len(arr) - 1)
        draw_callback(arr, "green")

    def _merge_sort_anim(self, arr, draw_callback):
        def merge_sort(arr, left, right):
            if left < right:
                mid = (left + right) // 2
                merge_sort(arr, left, mid)
                merge_sort(arr, mid + 1, right)
                merge(arr, left, mid, right)
    
        def merge(arr, left, mid, right):
            L = arr[left:mid + 1]
            R = arr[mid + 1:right + 1]
            i = j = 0
            k = left

            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
                draw_callback(arr)
                time.sleep(self.animation_speed)

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
                draw_callback(arr)
                time.sleep(self.animation_speed)

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
                draw_callback(arr)
                time.sleep(self.animation_speed)

        merge_sort(arr, 0, len(arr) - 1)
        draw_callback(arr, "green")

    def _open_competition(self):
        SortCompetitionFrame(self.root, self.algorithms)    

if __name__ == "__main__":
    root = ctk.CTk()
    app = SortingAppWithSeaborn(root)
    root.mainloop()


class SortCompetitionFrame(ctk.CTkToplevel):
    def __init__(self, master, algorithms):
        super().__init__(master)
        self.title("Compétition de Tri")
        CYBER_BG = "#2b2b2b"  # Define a default background color
        CYBER_TEXT = "#ffffff"  # Define a default text color
        self.configure(bg=CYBER_BG)
        self.geometry("800x600")
        self.algorithms = algorithms

        ctk.CTkLabel(self, text="Compétition de Tri", font=("Consolas", 22, "bold")).pack(pady=10)

        self.slider = ctk.CTkSlider(self, from_=1000, to=100000, number_of_steps=100, command=self._update_slider_label)
        self.slider.set(5000)
        self.slider.pack()
        self.slider_label = ctk.CTkLabel(self, text="Taille de la liste : 5000")
        self.slider_label.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Lancer la compétition", command=self._start_competition)
        self.start_button.pack(pady=10)



        self.tree = ttk.Treeview(self, columns=("Algorithme", "Temps (s)"), show="headings")
        self.tree.heading("Algorithme", text="Algorithme")
        self.tree.heading("Temps (s)", text="Temps (s)")
        self.tree.pack(fill="x", padx=20, pady=10)

        self.export_button = ctk.CTkButton(self, text="Exporter les résultats (CSV)", command=self._export_csv)
        self.export_button.pack(pady=5)

        self.save_button = ctk.CTkButton(self, text="Sauvegarder le graphique", command=self._save_plot)
        self.save_button.pack(pady=5)

        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _update_slider_label(self, val):
        self.slider_label.configure(text=f"Taille de la liste : {int(float(val))}")

    def _start_competition(self):
        threading.Thread(target=self._run_competition, daemon=True).start()

    def _run_competition(self):
        self.tree.delete(*self.tree.get_children())
        size = int(self.slider.get())
        base_data = [random.randint(1, 1000000) for _ in range(size)]
        results = []

        for name, algo in self.algorithms.items():
            data = base_data.copy()
            start = time.time()
            algo.sort(data)
            end = time.time()
            duration = round(end - start, 6)
            results.append((name, duration))

        results.sort(key=lambda x: x[1])
        for name, duration in results:
            self.tree.insert("", "end", values=(name, duration))

        # Affichage du graphique
        names = [r[0] for r in results]
        times = [r[1] for r in results]
        self.ax.clear()
        sns.barplot(x=times, y=names, ax=self.ax, palette="cool")
        self.ax.set_xlabel("Temps (s)")
        self.ax.set_ylabel("Algorithme")
        self.ax.set_title("Temps d'exécution par algorithme")
        self.canvas.draw()

    def _export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithme", "Temps (s)"])
            for row in self.tree.get_children():
                values = self.tree.item(row)["values"]
                writer.writerow(values)

    def _save_plot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.png")])
        if not file_path:
            return
        self.fig.savefig(file_path)

