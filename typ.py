import time
import random
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclipimg as pci
from pathlib import Path
import os
from PIL import ImageGrab
import pytesseract
import threading
import threading
import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

kb = Controller()

running = False
mode = None
delay_ms = 50  # фиксированная задержка между символами
words_list = []
photo_path = None

last_words = []
cycle_count = 0
error_chance = 0.05  # фиксированный шанс ошибки 10%


def maybe_swap_adjacent_letters(word, typo_chance=0.4):
    if len(word) < 2 or random.random() > typo_chance:
        return word
    i = random.randint(0, len(word) - 2)
    lst = list(word)
    lst[i], lst[i + 1] = lst[i + 1], lst[i]
    return ''.join(lst)


def type_word(word):
    global delay_ms
    for ch in word:
        kb.press(ch)
        kb.release(ch)
        time.sleep(delay_ms / 1000)
    kb.press(Key.enter)
    kb.release(Key.enter)


def get_random_word():
    global words_list, last_words
    if not words_list:
        print("Список слов пуст.")
        return None

    attempts = 0
    word = random.choice(words_list)
    while word in last_words[-2:] and attempts < 10:
        word = random.choice(words_list)
        attempts += 1

    last_words.append(word)
    if len(last_words) > 3:
        last_words.pop(0)
    return maybe_swap_adjacent_letters(word)


def type_random_word_with_typo():
    word = get_random_word()
    if word:
        print(f"Печать слова: {word}")
        type_word(word)


def send_photo_with_text():
    global photo_path
    if not photo_path:
        print("Путь до фото не указан.")
        return
    photo_file = Path(photo_path)
    if not photo_file.is_file():
        photo_file = Path(os.getcwd()) / photo_file.name
        if not photo_file.is_file():
            print(f"Фото {photo_path} не найдено по полному пути и в папке с ботом.")
            return
        else:
            print(f"Фото не найдено по полному пути, используем из папке с ботом: {photo_file}")

    try:
        pci.copy(photo_file)
        time.sleep(0.3)
        with kb.pressed(Key.ctrl):
            kb.press('v')
            kb.release('v')
        time.sleep(0.3)
        word = get_random_word()
        if word:
            type_word(word)
    except Exception as e:
        print(f"Ошибка при работе с фото или вставкой: {e}")


def worker():
    global running, mode, cycle_count
    while running:
        cycle_count += 1
        
        # Проверяем, произошла ли ошибка (фиксированный шанс)
        if random.random() < error_chance:
            print(f"[WARNING] Симулированная ошибка (пропуск цикла) - шанс {error_chance:.2%}")
            continue

        if mode == 1:
            type_random_word_with_typo()
        if mode == 2:
            send_photo_with_text()



def on_press(key):
    global running

    if key == Key.f1:
        if not running:
            print("Запуск.")
            running = True
            thread = threading.Thread(target=worker, daemon=True)
            thread.start()
        else:
            print("Уже запущено.")
    elif key == Key.f2:
        if running:
            print("Остановка.")
            running = False
        else:
            print("Не запущено.")


def main():
    global mode, delay_ms, words_list, photo_path
    choice = input("Выберите режим:\n1 - автотайпер из messages.txt\n2 - отправка фото и текста\nВведите 1 или 2: ").strip()
    if choice == '1':
        mode = 1
        try:
            with open("messages.txt", "r", encoding="utf-8") as f:
                content = f.read()
            words_list = content.split("\n")
            print(f"Загружено {len(words_list)} слов.")
        except Exception as e:
            print(f"Ошибка чтения messages.txt: {e}")
            return
    elif choice == '2':
        mode = 2
        photo_path = input("Введите полный путь до фото файла: ").strip()
        try:
            with open("messages.txt", "r", encoding="utf-8") as f:
                content = f.read()
            words_list = content.split("\n")
            print(f"Загружено {len(words_list)} слов для текста.")
        except Exception as e:
            print(f"Ошибка чтения messages.txt: {e}")
            return
    else:
        print("Неверный выбор.")
        return

    try:
        delay_ms = int(input("Введите задержку между символами в миллисекундах (например, 50): ").strip())
    except:
        delay_ms = 50
        print("Некорректный ввод. Установлена задержка 50 мс.")

    print("Нажмите F1 для запуска, F2 для остановки.")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()