
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import threading
import time
from sorting import HeapSort, CombSort, QuickSort, MergeSort

class SortingAppWithSeaborn:
    def __init__(self, root):
        self.root = root
        self.root.title("Tri Dynamique avec Seaborn")
        self.root.geometry("1000x700")
        self.root.configure(bg="#F5F5F5")
        ctk.set_appearance_mode("light")

        self.algorithms = {
            "Tri par tas": HeapSort(),
            "Tri à peigne": CombSort(),
            "Tri rapide": QuickSort(),
            "Tri fusion": MergeSort()
        }

        self._setup_ui()

    def _setup_ui(self):
        self.title_label = ctk.CTkLabel(self.root, text="Visualisation Dynamique de Tri", font=("Arial", 24, "bold"))
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

        self.canvas_frame = ctk.CTkFrame(self.root)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def _update_slider_label(self, val):
        self.slider_label.configure(text=f"Taille de la liste : {int(float(val))}")

    def _start_sorting(self):
        threading.Thread(target=self._run_sorting, daemon=True).start()

    def _run_sorting(self):
        n = int(self.slider.get())
        data = [random.randint(1, 100) for _ in range(n)]
        algo_name = self.algo_choice.get()
        algorithm = self.algorithms[algo_name]
        self._animate_sort(data, algorithm)

    def _animate_sort(self, data, algorithm):
        def update_plot(data, color="skyblue"):
            self.ax.clear()
            sns.barplot(x=list(range(len(data))), y=data, ax=self.ax, palette=[color]*len(data))
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
                    def draw_step():
                        update_plot(arr)
                        time.sleep(0.01)
                    self_inner.draw_step = draw_step
                    super(self_inner.__class__, self_inner).sort(arr)
            animated_algo = AnimatedAlgo()
            animated_algo.sort(data)
            update_plot(data, "green")

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
                    time.sleep(0.01)
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            draw_callback(arr)
            time.sleep(0.01)
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
                time.sleep(0.01)

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
                draw_callback(arr)
                time.sleep(0.01)

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
                draw_callback(arr)
                time.sleep(0.01)

        merge_sort(arr, 0, len(arr) - 1)
        draw_callback(arr, "green")

if __name__ == "__main__":
    root = ctk.CTk()
    app = SortingAppWithSeaborn(root)
    root.mainloop()
