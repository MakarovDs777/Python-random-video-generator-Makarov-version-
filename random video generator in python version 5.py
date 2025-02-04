import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import pygame
import threading

# Инициализация Pygame
pygame.mixer.init()

# Параметры
video_window = None
canvas = None

# Начальные координаты и сид
x, y, z = 0, 0, 0
seed = 42

def generate_random_audio(sample_rate=44100, duration=1):
    audio_data = np.random.uniform(-1, 1, int(sample_rate * duration)).astype(np.float32)
    return audio_data

def generate_random_video(seed, width=640, height=480):
    np.random.seed(seed)
    return np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

def play_sound():
    sample_rate = 44100
    while True:
        sound = generate_random_audio(sample_rate)
        sound = (sound * 32767).astype(np.int16)
        pygame.mixer.Sound(buffer=sound.tobytes()).play()
        pygame.time.delay(100)

def display_video():
    global video_window, canvas
    video_window = tk.Toplevel()
    video_window.title("Random Video")

    canvas = tk.Canvas(video_window, width=640, height=480)
    canvas.pack()

    update_frame()  # Первый кадр

def start_audio_and_video():
    thread = threading.Thread(target=play_sound, daemon=True)
    thread.start()
    display_video()

def update_frame():
    if canvas:
        # Генерация нового сида на основе координат и текущего сида из поля
        current_seed = (x * 10000 + y * 100 + z + seed) % (2**32)
        frame = generate_random_video(current_seed)  # Генерация нового кадра с использованием сида
        frame_image = Image.fromarray(frame)
        frame_image = ImageTk.PhotoImage(frame_image)

        # Обновление Canvas
        canvas.delete('all')
        canvas.create_image(0, 0, anchor=tk.NW, image=frame_image)
        canvas.image = frame_image  # Сохраняем ссылку для предотвращения сборки мусора

def update_coordinates_display():
    coordinates_label.config(text=f"Координаты - x: {x}, y: {y}, z: {z}, Seed: {seed}")

def move_left():
    global x
    x -= 1
    update_frame()
    update_coordinates_display()

def move_right():
    global x
    x += 1
    update_frame()
    update_coordinates_display()

def move_up():
    global y
    y += 1
    update_frame()
    update_coordinates_display()

def move_down():
    global y
    y -= 1
    update_frame()
    update_coordinates_display()

def set_seed():
    global seed
    try:
        seed = int(seed_entry.get())
        update_frame()  # Обновление кадра с новым сидом
        update_coordinates_display()  # Обновление отображения координат
    except ValueError:
        seed_entry.delete(0, tk.END)
        seed_entry.insert(0, str(seed))  # Восстановление введённого значения, если ввод некорректен

def validate_seed_input(event):
    current_value = seed_entry.get()
    if not current_value.isdigit():
        seed_entry.delete(0, tk.END)
        seed_entry.insert(0, ''.join(filter(str.isdigit, current_value)))  # Удалить некорректные символы

# Создание основного окна
root = tk.Tk()
root.title("Procedural Audio and Video")
root.geometry("320x200")

start_button = tk.Button(root, text="Start", command=start_audio_and_video)
start_button.pack()

coordinates_label = tk.Label(root, text=f"Координаты - x: {x}, y: {y}, z: {z}, Seed: {seed}")
coordinates_label.pack()

seed_entry = tk.Entry(root)
seed_entry.pack()
seed_entry.insert(0, str(seed))  # Ввод сида по умолчанию

seed_entry.bind('<KeyRelease>', validate_seed_input)  # Проверка ввода сида

set_seed_button = tk.Button(root, text="Установить сид", command=set_seed)
set_seed_button.pack()

# Добавление кнопок для перемещения
move_buttons_frame = tk.Frame(root)
move_buttons_frame.pack()

left_button = tk.Button(move_buttons_frame, text="Left", command=move_left)
left_button.grid(row=0, column=0)

right_button = tk.Button(move_buttons_frame, text="Right", command=move_right)
right_button.grid(row=0, column=2)

up_button = tk.Button(move_buttons_frame, text="Up", command=move_up)
up_button.grid(row=1, column=1)

down_button = tk.Button(move_buttons_frame, text="Down", command=move_down)
down_button.grid(row=2, column=1)

# Запуск основного цикла интерфейса
root.mainloop()
