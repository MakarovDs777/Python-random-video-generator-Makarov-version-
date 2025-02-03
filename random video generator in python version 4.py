import tkinter as tk
from tkinter import filedialog
import os
import random
import numpy as np
import pygame
from threading import Thread
from pydub import AudioSegment
from PIL import Image, ImageTk

def convert_audio_to_bytes(path):
    audio = AudioSegment.from_file(path)  # Загружаем аудиофайл
    return audio.raw_data, audio.frame_rate  # Возвращаем сырые данные и частоту дискретизации

def mix_audio_bytes(audio_data):
    # Преобразуем сырье в список байтов
    byte_list = list(audio_data)

    # Перемешивание байтов
    random.shuffle(byte_list)
    
    # Возвращаем перемешанные данные
    return bytes(byte_list)

def play_sound(shuffled_audio, sample_rate):
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
    sound = pygame.mixer.Sound(buffer=shuffled_audio)
    sound.play(-1)  # Воспроизведение звука зациклено

def display_video():
    video_window = tk.Toplevel()
    video_window.title("Random Video")

    canvas = tk.Canvas(video_window, width=640, height=480)
    canvas.pack()

    def update_frame():
        frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        frame_image = Image.fromarray(frame)
        frame_image = ImageTk.PhotoImage(frame_image)

        canvas.create_image(0, 0, anchor=tk.NW, image=frame_image)
        canvas.image = frame_image  # Сохранение ссылки на изображение
        video_window.after(10, update_frame)  # Непрерывное обновление

    update_frame()  # Запуск обновления

def start_audio_and_video():
    audio_file_path = filedialog.askopenfilename(
        title="Выберите аудио файл", 
        filetypes=[("Audio Files", "*.wav;*.mp3;*.ogg;*.flac")]  # Поддержка различных форматов
    )
    if audio_file_path:
        audio_data, sample_rate = convert_audio_to_bytes(audio_file_path)

        # Перемешивание байтов аудио
        shuffled_audio = mix_audio_bytes(audio_data)

        # Запуск воспроизведения
        Thread(target=play_sound, args=(shuffled_audio, sample_rate), daemon=True).start()
        
        display_video()  # Запуск отображения видео в новом окне

# Создание графического интерфейса
root = tk.Tk()
root.title("Procedural Audio Mixer")
root.geometry("320x120")  # Установка размера окна

start_button = tk.Button(root, text="Start", command=start_audio_and_video)
start_button.pack(pady=20)

# Запустить основной цикл интерфейса
root.mainloop()
