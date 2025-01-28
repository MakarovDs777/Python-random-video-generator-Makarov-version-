import tkinter as tk
import numpy as np
import pygame
from threading import Thread
from PIL import Image, ImageTk

# Параметры перемещения
move_speed = 1
current_frame_index = 0

def generate_random_audio(sample_rate=44100, duration=1):
    audio_data = np.random.uniform(-1, 1, int(sample_rate * duration)).astype(np.float32)
    return audio_data

def play_sound():
    sample_rate = 44100
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
    while True:
        sound = generate_random_audio(sample_rate)
        sound = (sound * 32767).astype(np.int16)
        pygame.mixer.Sound(buffer=sound.tobytes()).play()
        pygame.time.delay(100)

def generate_random_video(width=640, height=480):
    return np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

def display_video():
    video_window = tk.Toplevel()
    video_window.title("Random Video")

    canvas = tk.Canvas(video_window, width=640, height=480)
    canvas.pack()

    def update_frame():
        frame = generate_random_video()
        frame_image = Image.fromarray(frame)
        frame_image = ImageTk.PhotoImage(frame_image)

        canvas.create_image(0, 0, anchor=tk.NW, image=frame_image)
        canvas.image = frame_image
        video_window.after(10, update_frame)

    update_frame()

def start_audio_and_video():
    Thread(target=play_sound, daemon=True).start()
    display_video()

def move_camera(direction):
    global current_frame_index
    # При нажатии увеличиваем/уменьшаем индекс кадра
    if direction == "F":  # Вперед
        current_frame_index += move_speed
    elif direction == "B":  # Назад
        current_frame_index -= move_speed
    elif direction == "L":  # Перезапускаем видео (прошлый кадр)
        current_frame_index = max(0, current_frame_index - 1)
    elif direction == "R":  # Следующий кадр
        current_frame_index += move_speed

    # Обновление видео (в данном случае просто генерация нового)
    display_new_frame(current_frame_index)

def display_new_frame(index):
    # Логика для отображения нового кадра по индексу
    print(f"Текущий кадр: {index}")

def on_key_press(event):
    key = event.keysym
    if key == 'w':
        move_camera("F")
    elif key == 's':
        move_camera("B")
    elif key == 'a':
        move_camera("L")
    elif key == 'd':
        move_camera("R")
    elif key == 'q':
        move_camera("L")  # Аналог перемещения назад
    elif key == 'e':
        move_camera("R")  # Аналог перемещения вперед

# Создание графического интерфейса
root = tk.Tk()
root.title("Procedural Audio and Video Generator")
root.geometry("320x120")

start_button = tk.Button(root, text="Start", command=start_audio_and_video)
start_button.pack()

root.bind("<KeyPress>", on_key_press)  # Привязываем обработчик к событиям клавиш

# Запустить основной цикл интерфейса
root.mainloop()
