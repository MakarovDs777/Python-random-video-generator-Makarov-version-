import numpy as np
import cv2
import sounddevice as sd

def generate_random_video_with_sound(width, height):

    # Функция для генерации случайного видео с изменяющимися параметрами на каждой итерации
    # Начальные параметры
    colors = np.random.randint(0, 256, (height * width, 3)) # Радуга цветов
    np.random.shuffle(colors)
    frame_count = 0

    # Звуковые параметры
    sample_rate = 44100  # Частота дискретизации
    duration = 1.0  # Длительность звука в секундах
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)  # Временная шкала
    frequency = 440  # Начальная частота (A4)

    while True:

        # Генерация кадра
        frame = np.ones((height, width, 3), dtype=np.uint8) * 255 # Белый фон

        # Изменение параметров
        np.random.shuffle(colors) # Перемешиваем цвета

        # Рисуем случайные пиксели с радуги цветов
        for i in range(height):
            for j in range(width):
                frame[i][j] = colors[i * width + j]

        yield frame

        # Усложнение параметров на каждой итерации
        frame_count += 1
        if frame_count % 100 == 0:
            # Каждые 100 кадров увеличиваем амплитуду изменения параметров
            pass

        # Генерация случайного звука
        frequency = np.random.uniform(100, 1000)  # Генерируем случайную частоту
        waveform = np.sin(2 * np.pi * frequency * t)  # Синусоидальная волна

        # Воспроизведение звука
        sd.play(waveform, samplerate=sample_rate, blocking=True)

if __name__ == "__main__":
    width = 1280 # Ширина видео
    height = 720 # Высота видео

    # Генерация видео на ходу с звуком
    frames_generator = generate_random_video_with_sound(width, height)

    # Отображение видео в отдельном окне
    for frame in frames_generator:
        cv2.imshow("Random Video with Sound", frame)
        if cv2.waitKey(int(1000/30)) & 0xFF == ord('q'): # Нажмите 'q', чтобы выйти из цикла
            break

    cv2.destroyAllWindows()
