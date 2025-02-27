import random
from PIL import Image, ImageTk
import tkinter as tk

class InfiniteNoiseImage:
    def __init__(self):
        self.image_size = (800, 600)  # Размер изображения
        self.total_pixels = self.image_size[0] * self.image_size[1]  # Общее количество пикселей
        self.x, self.y = 0, 0  # Начальные координаты
        self.seed = random.randint(0, 10000)  # Случайный сид
        self.frames = 10  # Количество кадров для генерации
        self.current_frame_index = 0  # Индекс текущего кадра
        self.rgb_values = self.generate_rgb_values()  # Генерация значений RGB на основе сида
        self.is_moving = False  # Инициализируем переменную для автоматического перемещения

        self.root = tk.Tk()
        self.root.title("Infinite Noise Image")

        self.canvas = tk.Canvas(self.root, width=self.image_size[0], height=self.image_size[1])
        self.canvas.pack()

        # Метка для отображения координат
        self.coordinates_label = tk.Label(self.root, text=f"Координаты - X: {self.x}, Y: {self.y}, Seed: {self.seed}")
        self.coordinates_label.pack()

        # Панель с полями ввода и кнопками (в одну строку)
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(side="top", anchor="w", pady=(10, 0))

        # Поля ввода для координат
        tk.Label(controls_frame, text="X:").grid(row=0, column=0)
        self.x_entry = tk.Entry(controls_frame, width=5)
        self.x_entry.grid(row=0, column=1)
        self.x_entry.insert(0, str(self.x))

        tk.Label(controls_frame, text="Y:").grid(row=0, column=2)
        self.y_entry = tk.Entry(controls_frame, width=5)
        self.y_entry.grid(row=0, column=3)
        self.y_entry.insert(0, str(self.y))

        tk.Label(controls_frame, text="Сид:").grid(row=0, column=4)
        self.seed_entry = tk.Entry(controls_frame, width=10)
        self.seed_entry.grid(row=0, column=5)
        self.seed_entry.insert(0, str(self.seed))

        set_coordinates_button = tk.Button(controls_frame, text="Установить координаты", command=self.set_coordinates)
        set_coordinates_button.grid(row=0, column=6)

        set_seed_button = tk.Button(controls_frame, text="Установить сид", command=self.set_seed)
        set_seed_button.grid(row=0, column=7)

        tk.Label(controls_frame, text="Скорость обновления (мс):").grid(row=0, column=8)
        self.speed_entry = tk.Entry(controls_frame, width=5)
        self.speed_entry.grid(row=0, column=9)
        self.speed_entry.insert(0, "1000")

        # Кнопки для управления
        self.update_button = tk.Button(controls_frame, text="Сгенерировать изображение", command=self.update_image)
        self.update_button.grid(row=0, column=10, padx=(5, 0))

        self.move_button = tk.Button(controls_frame, text="Авто-обновление", command=self.toggle_auto_move)
        self.move_button.grid(row=0, column=11, padx=(5, 0))

        # Добавление кнопок для перемещения
        left_button = tk.Button(controls_frame, text="←", command=self.move_left)
        left_button.grid(row=0, column=12, padx=(5, 0))

        up_button = tk.Button(controls_frame, text="↑", command=self.move_up)
        up_button.grid(row=0, column=13, padx=(5, 0))

        down_button = tk.Button(controls_frame, text="↓", command=self.move_down)
        down_button.grid(row=0, column=14, padx=(5, 0))

        right_button = tk.Button(controls_frame, text="→", command=self.move_right)
        right_button.grid(row=0, column=15, padx=(5, 0))

        self.image = Image.new('RGB', self.image_size)

        self.root.mainloop()

    def generate_rgb_values(self):
        # Генерация RGB значений по заданному сиду для каждого кадра
        rgb_values = []

        for frame in range(self.frames):
            random.seed(self.seed + frame)  # Устанавливаем сид для каждого кадра
            frame_rgb = []
            
            for i in range(self.total_pixels):
                # Генерация по порядку без повторений (в данном случае 3-значные последовательности)
                r = (i * 3) % 256
                g = (i * 3 + 1) % 256
                b = (i * 3 + 2) % 256
                frame_rgb.append((r, g, b))
            
            rgb_values.append(frame_rgb)
        
        return rgb_values

    def update_image(self):
        frame_rgb_colors = self.rgb_values[self.current_frame_index % self.frames]  # Получаем цвета для текущего кадра
        
        for i in range(len(frame_rgb_colors)):
            x = i % self.image_size[0]  # Вычисляем X-координату
            y = i // self.image_size[0]  # Вычисляем Y-координату
            self.image.putpixel((x, y), frame_rgb_colors[i])
        
        self.update_canvas()
        self.update_coordinates_display()  # Обновление отображения координат
        self.current_frame_index += 1  # Переходим к следующему кадру

    def update_canvas(self):
        image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        self.canvas.image = image_tk  # Сохранение ссылки на изображение

    def update_coordinates_display(self):
        self.coordinates_label.config(text=f"Координаты - X: {self.x}, Y: {self.y}, Seed: {self.seed}")

    def set_coordinates(self):
        try:
            self.x = int(self.x_entry.get())
            self.y = int(self.y_entry.get())
            self.update_image()  # Обновляем изображение при изменении координат
            self.update_coordinates_display()  # Обновляем отображение координат
        except ValueError:
            # Игнорировать некорректные значения
            pass

    def set_seed(self):
        try:
            self.seed = int(self.seed_entry.get())
            self.rgb_values = self.generate_rgb_values()  # Генерация новых значений RGB на основе нового сида
            self.update_image()  # Обновляем изображение
        except ValueError:
            # Игнорировать некорректные значения
            pass

    def toggle_auto_move(self):
        if self.is_moving:
            self.is_moving = False
            self.move_button.config(text="Авто-обновление")
        else:
            self.is_moving = True
            self.move_button.config(text="Остановить обновление")
            self.auto_move()

    def auto_move(self):
        if self.is_moving:
            delta_x = random.randint(-10, 10)  # Случайный сдвиг по X
            delta_y = random.randint(-10, 10)  # Случайный сдвиг по Y
            self.x += delta_x
            self.y += delta_y
            
            self.update_coordinates_display()  # Обновляем табло координат при движении
            self.update_image()  # Обновляем изображение с новыми координатами

            speed = int(self.speed_entry.get()) if self.speed_entry.get().isdigit() else 1000
            self.root.after(speed, self.auto_move)  # Обновление через `speed` мс

    def move_left(self):
        self.x -= 1
        self.update_coordinates_display()  # Обновляем табло координат после изменения позиции
        self.update_image()

    def move_right(self):
        self.x += 1
        self.update_coordinates_display()  # Обновляем табло координат после изменения позиции
        self.update_image()

    def move_up(self):
        self.y += 1
        self.update_coordinates_display()  # Обновляем табло координат после изменения позиции
        self.update_image()

    def move_down(self):
        self.y -= 1
        self.update_coordinates_display()  # Обновляем табло координат после изменения позиции
        self.update_image()

# Пример использования
InfiniteNoiseImage()
