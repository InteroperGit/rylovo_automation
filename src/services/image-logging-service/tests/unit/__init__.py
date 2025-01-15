import os
import sys

# Определяем базовую директорию относительно текущего файла
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))

# Добавляем необходимые пути
paths = [
    os.path.join(base_dir, 'src/services/image-logging-service/tests/unit'),
    os.path.join(base_dir, 'src/services/image-logging-service/src'),
    os.path.join(base_dir, 'src/libs/python')
]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)