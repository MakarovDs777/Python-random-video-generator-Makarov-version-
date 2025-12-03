import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import os
from datetime import datetime
import threading
import time

try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

# Храним последний сгенерированный массив и сид
last_array = None
last_seed = None

# Состояние EGF Video
_egf_video_window = None
_egf_video_running = False
_egf_video_stop_event = None

# Функция для генерации массива случайных чисел (0..255)
def generate_random_array(seed, length):
    rng = np.random.RandomState(int(seed) & 0xFFFFFFFF)
    return rng.randint(0, 256, size=length).tolist()

# Обработчик кнопки "Генерировать"
def on_generate():
    global last_array, last_seed

    seed_str = entry_seed.get().strip()
    length_str = entry_length.get().strip()

    if not seed_str:
        messagebox.showwarning("Ошибка", "Введите номер сида.")
        return

    try:
        seed = int(seed_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Сид должен быть целым числом.")
        return

    try:
        length = int(length_str)
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Длина должна быть положительным целым числом.")
        return

    arr = generate_random_array(seed, length)
    last_array = arr
    last_seed = seed

    output_text.config(state='normal')
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"Сид: {seed}\nМассив ({length}): {arr}\n")
    output_text.config(state='disabled')

    # Активируем кнопку сохранения
    btn_save.config(state='normal')


# Обработчик кнопки "Сохранить"
def on_save():
    global last_array, last_seed

    if not last_array:
        messagebox.showwarning("Нет данных", "Сначала сгенерируйте массив.")
        return

    # Формируем строку с числами через пробел
    content = ' '.join(map(str, last_array))

    # Пытаемся сохранить на рабочий стол
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    if not os.path.isdir(desktop):
        # Если папка рабочего стола не найдена, используем текущую директорию
        desktop = os.getcwd()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if last_seed is not None:
        filename = f"array_seed_{last_seed}_{timestamp}.txt"
    else:
        filename = f"array_{timestamp}.txt"

    path = os.path.join(desktop, filename)

    try:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
    except Exception as e:
        messagebox.showerror("Ошибка записи", f"Не удалось сохранить файл:\n{e}")
        return

    messagebox.showinfo("Сохранено", f"Файл сохранён:\n{path}")


# --- EGF Video: генерация бесконечной трансляции по сиду ---
def start_egf_video_from_seed(root, seed, width, height, fps):
    global _egf_video_window, _egf_video_running, _egf_video_stop_event

    if Image is None or ImageTk is None:
        messagebox.showerror("Зависимость отсутствует", "Требуется библиотека Pillow (PIL). Установите её: pip install pillow")
        return

    if _egf_video_running:
        messagebox.showwarning("Уже запущено", "EGF Video уже запущено.")
        return

    try:
        seed = int(seed)
        width = int(width)
        height = int(height)
        fps = int(fps)
        if width <= 0 or height <= 0 or fps <= 0:
            raise ValueError
    except Exception:
        messagebox.showerror("Ошибка параметров", "Неверные параметры видео (ширина, высота, fps).")
        return

    win = tk.Toplevel(root)
    win.title(f"EGF Video — seed={seed}")
    canvas = tk.Canvas(win, width=width, height=height)
    canvas.pack()

    stop_event = threading.Event()
    _egf_video_stop_event = stop_event
    _egf_video_window = win
    _egf_video_running = True

    rng = np.random.RandomState(int(seed) & 0xFFFFFFFF)

    # Генерация и отрисовка кадра в main thread с помощью after — чтобы не блокировать UI
    def render_frame():
        if stop_event.is_set():
            try:
                win.destroy()
            except Exception:
                pass
            return
        # Генерируем кадр: последовательные байты из RNG, упакованные по RGB
        try:
            arr = rng.randint(0, 256, (height, width, 3), dtype=np.uint8)
            img = Image.fromarray(arr, 'RGB')
            photo = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            # сохранить ссылку, чтобы изображение не было удалено сборщиком мусора
            canvas.image = photo
        except Exception:
            pass
        # планируем следующий кадр
        win.after(int(1000 / max(1, fps)), render_frame)

    # Обработчик закрытия окна — ставим событие остановки
    def on_close():
        stop_event.set()
        try:
            win.destroy()
        except Exception:
            pass

    win.protocol("WM_DELETE_WINDOW", on_close)
    render_frame()


# GUI: создание окна
root = tk.Tk()
root.title("Генератор массива по сиду + EVP Video")
root.geometry("420x420")  # Установка размера окна

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Поле для ввода сида
lbl_seed = tk.Label(frame, text="Сид:")
lbl_seed.grid(row=0, column=0, sticky='w')
entry_seed = tk.Entry(frame, width=20)
entry_seed.grid(row=0, column=1, padx=(5, 0))

# Поле для ввода длины массива
lbl_length = tk.Label(frame, text="Длина массива:")
lbl_length.grid(row=1, column=0, sticky='w', pady=(6,0))
entry_length = tk.Entry(frame, width=20)
entry_length.grid(row=1, column=1, padx=(5, 0), pady=(6,0))
entry_length.insert(0, "5")  # значение по умолчанию

# Кнопка генерации
btn_gen = tk.Button(frame, text="Генерировать", command=on_generate)
btn_gen.grid(row=2, column=0, columnspan=2, pady=(10,0), sticky='ew')

# Кнопка сохранения
btn_save = tk.Button(frame, text="Сохранить на рабочий стол", command=on_save, state='disabled')
btn_save.grid(row=3, column=0, columnspan=2, pady=(6,0), sticky='ew')

# Разделитель
sep = tk.Frame(frame, height=2, bd=1, relief=tk.SUNKEN)
sep.grid(row=4, column=0, columnspan=2, pady=(10,6), sticky='ew')

# Параметры видео
lbl_vw = tk.Label(frame, text="Video width:")
lbl_vw.grid(row=5, column=0, sticky='w')
entry_vw = tk.Entry(frame, width=10)
entry_vw.grid(row=5, column=1, sticky='w')
entry_vw.insert(0, "320")

lbl_vh = tk.Label(frame, text="Video height:")
lbl_vh.grid(row=6, column=0, sticky='w')
entry_vh = tk.Entry(frame, width=10)
entry_vh.grid(row=6, column=1, sticky='w')
entry_vh.insert(0, "240")

lbl_fps = tk.Label(frame, text="FPS:")
lbl_fps.grid(row=7, column=0, sticky='w')
entry_fps = tk.Entry(frame, width=10)
entry_fps.grid(row=7, column=1, sticky='w')
entry_fps.insert(0, "20")

# Кнопка запуска EGF Video
def on_egf_video_button():
    global _egf_video_running, _egf_video_stop_event
    if _egf_video_running:
        if _egf_video_stop_event:
            _egf_video_stop_event.set()
        _egf_video_running = False
        messagebox.showinfo("Остановлено", "EGF Video остановлено.")
        return

    seed = entry_seed.get().strip()
    if not seed:
        messagebox.showwarning("Ошибка", "Введите сид для трансляции.")
        return
    width = entry_vw.get().strip()
    height = entry_vh.get().strip()
    fps = entry_fps.get().strip()

    # Открыть окно и стартовать трансляцию
    _egf_video_stop_event = threading.Event()
    # Используем render в main thread, поэтому просто вызовем функцию
    start_egf_video_from_seed(root, seed, width, height, fps)

btn_egf_video = tk.Button(frame, text="EGF Video (по сиду) — Старт/Останов", command=on_egf_video_button)
btn_egf_video.grid(row=8, column=0, columnspan=2, pady=(10,0), sticky='ew')

# Табло/вывод
lbl_out = tk.Label(frame, text="Результат:")
lbl_out.grid(row=9, column=0, columnspan=2, sticky='w', pady=(10,0))

output_text = scrolledtext.ScrolledText(frame, width=40, height=6, state='disabled')
output_text.grid(row=10, column=0, columnspan=2, pady=(4,0))

# Привязка клавиши Enter к генерации
root.bind('<Return>', lambda event: on_generate())

# Запуск приложения
if __name__ == '__main__':
    root.mainloop()
