import sys
import os
from pathlib import Path

with open("path.txt", 'r') as f:
    folder_path = f.readline().strip()

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Удалён файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при удалении {file_path}: {e}")
