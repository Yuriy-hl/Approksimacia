import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import numpy as np
import json
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class DataApproximationApp:
    def __init__(self, root):
        self.coefficients = None
        self.error = None
        self.canvas = None
        self.root = root
        self.root.title("Data Approximation App")

        # Создание элементов интерфейса
        self.label = ttk.Label(root, text="Выберите файл с данными:")
        self.label.pack(pady=10)

        self.load_button = ttk.Button(root, text="Загрузить данные", command=self.load_data)
        self.load_button.pack()

        # Добавление элементов для выбора степени полинома
        self.degree_label = ttk.Label(root, text="Введите степень полинома:")
        self.degree_label.pack(pady=10)

        self.degree_entry = tk.Entry(root)
        self.degree_entry.pack()

        self.approximate_button = ttk.Button(root, text="Провести аппроксимацию", command=self.approximate_data)
        self.approximate_button.pack(pady=10)

        # Добавление кнопок для сохранения графика и коэффициентов
        self.save_plot_button = ttk.Button(root, text="Сохранить график", command=self.save_plot)
        self.save_plot_button.pack(pady=10)

        self.save_coefficients_button = ttk.Button(root, text="Сохранить коэффициенты и погрешности",
                                                   command=self.save_coefficients)
        self.save_coefficients_button.pack(pady=10)

        self.x = []
        self.y = []

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.x = data['x']
                self.y = data['y']

    def approximate_data(self):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()  # Удаление предыдущего графика
        degree_str = self.degree_entry.get()
        if int(degree_str) < 0:
            return print("Степень полинома не может быть отрицательной.")
        if not degree_str:
            print("Степень полинома не введена.")
            return
        try:
            degree = int(degree_str)

        except ValueError:
            print("Степень полинома должна быть целым числом.")
            return
        if len(self.x) == 0 or len(self.y) == 0:
            print("Данные отсутствуют. Загрузите данные перед проведением аппроксимации.")
            return
        coefficients, residuals, _, _, _ = np.polyfit(self.x, self.y, degree, full=True, cov=True)
        poly = np.poly1d(coefficients)
        y_fit = poly(self.x)
        error = np.sqrt(np.mean((self.y - y_fit) ** 2))

        fig, ax = plt.subplots()
        ax.scatter(self.x, self.y, label='Экспериментальные данные')
        ax.plot(self.x, y_fit, label=f'Аппроксимация с полиномом {degree} степени')
        ax.legend()
        ax.set_title('Аппроксимация данных')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.coefficients = coefficients
        self.error = error

    def save_plot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            plt.savefig(file_path)

    def save_coefficients(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if self.coefficients is not None and self.error is not None:
            with open(file_path, 'w') as file:
                file.write('# Коэффициенты полинома\n')
                np.savetxt(file, self.coefficients, delimiter=',', newline='\n',
                           footer='# Погрешности: {:.6f}'.format(self.error))


root = tk.Tk()
app = DataApproximationApp(root)
root.mainloop()