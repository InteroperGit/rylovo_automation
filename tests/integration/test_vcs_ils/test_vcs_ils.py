import pytest
import os
import time
import subprocess
import cv2
import numpy as np
import glob
from typing import Optional, Generator

INPUT_DIR = "/tmp/input"
OUTPUT_DIR = "/tmp/output"
IMAGE_FILE_NAME = "test_image.jpg"
TEST_DATA = b"test_image_data"
IMAGE_SIZE = (300, 300, 3)

def clear_directory(directory: str) -> None:
    """
    Очищает каталог от всех файлов и пустых каталогов.

    :param directory: Путь к каталогу, который нужно очистить
    :return: None
    """
    for entry in os.scandir(directory):
        if entry.is_file():
            os.remove(entry.path)  # Удаляем файл
        elif entry.is_dir():
            clear_directory(entry.path)  # Рекурсивно очищаем вложенный каталог
            os.rmdir(entry.path)  # Удаляем пустой каталог

def create_image_file(file_name: str) -> None:
    """
    Создает черное изображение размером 300x300 пикселей и сохраняет его в файл.

    :param file_name: Путь к файлу, в который будет сохранено изображение
    :return: None
    """
    rectangle = np.zeros(IMAGE_SIZE, dtype=np.uint8)
    cv2.imwrite(file_name, rectangle)

def find_latest_image(directory: str) -> Optional[str]:
    """
    Находит последнее изображение (по времени модификации) в каталоге.

    :param directory: Путь к каталогу, в котором нужно искать изображения
    :return: Путь к последнему изображению или None, если файлы не найдены
    """
    files = glob.glob(os.path.join(directory, "**/*.jpg"), recursive=True)

    if not files:
        return None

    # Сортируем файлы по времени последней модификации
    files.sort(key=lambda x: os.path.getmtime(x))

    return files[-1]

def prepare_input_directory() -> None:
    """
    Подготавливает входной каталог: очищает его, если он существует, и создает новое изображение.

    :return: None
    """    
    
    if os.path.exists(INPUT_DIR):
        clear_directory(INPUT_DIR)
    else:
        os.makedirs(INPUT_DIR, exist_ok=True, mode=0o777)
        
    print(f"[Test_VCS_ILS] Input directory abs path: [{os.path.abspath(INPUT_DIR)}]")
        
    IMAGE_FILE_NAME = "test_image.jpg"
    
    input_file_path = os.path.join(INPUT_DIR, IMAGE_FILE_NAME)
    
    create_image_file(input_file_path)
        
    if os.path.exists(input_file_path):
        print(f"[Test_VCS_ILS] File [{input_file_path}] was created successfully")
    else:
        print(f"[Test_VCS_ILS] File [{input_file_path}] failed to create")

def prepare_output_directory() -> None:
    """
    Подготавливает выходной каталог: очищает его, если он существует, и создает новый каталог.

    :return: None
    """
    
    if os.path.exists(OUTPUT_DIR):
        clear_directory(OUTPUT_DIR)
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True, mode=0o777)

@pytest.fixture(scope="module", autouse=True)
def setup_environment() -> Generator[any, any, any]:
    """
    Настройка окружения для теста: подготовка входного и выходного каталогов,
    запуск Docker-контейнеров, ожидание их запуска, выполнение теста и остановка контейнеров.

    :return: Generator[any, any, any]
    """
    
    prepare_input_directory()
    prepare_output_directory()
    
    # Получаем каталог, в котором находится текущий исполняемый файл (тест)
    test_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Указываем путь к docker-compose.yml относительно каталога теста
    docker_compose_file = os.path.join(test_file_dir, "docker-compose.yml")

    print(f"[Test_VCS_ILS] docker_compose_file: {docker_compose_file}")

    # Запускаем docker-compose с явным указанием пути
    subprocess.run(["docker-compose", "-f", docker_compose_file, "up", "--build", "-d"], check=True)
        
    print(f"[Test_VCS_ILS] Docker compose was successfully started")
    
    time.sleep(20)
    
    subprocess.run(["docker-compose", "-f", docker_compose_file, "logs"], check=True)

    yield
    
    subprocess.run(["docker-compose", "-f", docker_compose_file, "down"], check=True)
    
    print(f"[Test_VCS_ILS] Docker compose was successfully stoped")
    
def test_image_processing() -> None:
    """
    Тестирование обработки изображения: находит последнее изображение в каталоге OUTPUT_DIR
    и проверяет, что оно существует и имеет правильный размер.

    :return: None
    """
    
    file_name = find_latest_image(OUTPUT_DIR)
    assert file_name is not None, f"Не найдены файлы в каталоге [{OUTPUT_DIR}]"
    
    img = cv2.imread(file_name)
    
    assert img is not None, f"Не удалось считать изображение [{file_name}]"
    assert img.shape == IMAGE_SIZE, f"Размер изображения {img.shape} не совпадает с эталонным {IMAGE_SIZE}"