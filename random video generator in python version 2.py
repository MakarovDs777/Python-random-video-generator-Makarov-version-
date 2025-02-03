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

def generate_random_audio(sample_rate=44100, duration=1):
    audio_data = np.random.uniform(-1, 1, int(sample_rate * duration)).astype(np.float32)
    return audio_data

def play_sound():
    sample_rate = 44100
    while True:
        sound = generate_random_audio(sample_rate)
        sound = (sound * 32767).astype(np.int16)
        pygame.mixer.Sound(buffer=sound.tobytes()).play()
        pygame.time.delay(100)

def generate_random_video(width=640, height=480):
    return np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

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
        frame = generate_random_video()  # Генерация нового случайного кадра
        frame_image = Image.fromarray(frame)
        frame_image = ImageTk.PhotoImage(frame_image)

        # Обновление Canvas
        canvas.delete('all')
        canvas.create_image(0, 0, anchor=tk.NW, image=frame_image)
        canvas.image = frame_image  # Сохраняем ссылку для предотвращения сборки мусора

def on_key_press(event):
    if event.keysym in ['q', 'w', 'e', 'a', 's', 'd']:
        update_frame()  # Обновление кадра при нажатии клавиш

# Создание основного окна
root = tk.Tk()
root.title("EVP space random")
root.geometry("320x120")

start_button = tk.Button(root, text="Start", command=start_audio_and_video)
start_button.pack()

root.bind('q', on_key_press)
root.bind('w', on_key_press)
root.bind('e', on_key_press)
root.bind('a', on_key_press)
root.bind('s', on_key_press)
root.bind('d', on_key_press)

# Запуск основного цикла интерфейса
root.mainloop()
