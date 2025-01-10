import os
import sys

# Определяем базовую директорию относительно текущего файла
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Добавляем необходимые пути
sys.path.append(os.path.join(base_dir, 'tests/unit'))
sys.path.append(os.path.join(base_dir, 'src'))
sys.path.append(os.path.join(base_dir, 'libs', 'python'))