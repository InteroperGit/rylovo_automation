import pytest
import os
import time
import subprocess
import cv2
import numpy as np
import glob

INPUT_DIR = "/tmp/input"
OUTPUT_DIR = "/tmp/output"
IMAGE_FILE_NAME = "test_image.jpg"
TEST_DATA = b"test_image_data"
IMAGE_SIZE = (300, 300, 3)

def clear_directory(directory):
    for entry in os.scandir(directory):
        if entry.is_file():
            os.remove(entry.path)  # Удаляем файл
        elif entry.is_dir():
            clear_directory(entry.path)  # Рекурсивно очищаем вложенный каталог
            os.rmdir(entry.path)  # Удаляем пустой каталог

def create_image_file(file_name: str) -> None:
    rectangle = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.imwrite(file_name, rectangle)

def find_latest_image(directory):
    files = glob.glob(os.path.join(directory, "**/*.jpg"), recursive=True)
    
    if not files:
        None
    
    files.sort(key=lambda x: os.path.getmtime(x))
    
    return files[-1]

def prepare_input_directory():
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

def prepare_output_directory():
    if os.path.exists(OUTPUT_DIR):
        clear_directory(OUTPUT_DIR)
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True, mode=0o777)

@pytest.fixture(scope="module", autouse=True)
def setup_environment():
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
    
def test_image_processing():
    file_name = find_latest_image(OUTPUT_DIR)
    assert file_name is not None, f"Не найдены файлы в каталоге [{OUTPUT_DIR}]"
    
    img = cv2.imread(file_name)
    
    assert img is not None, f"Не удалось считать изображение [{file_name}]"
    assert img.shape == IMAGE_SIZE, f"Размер изображения {img.shape} не совпадает с эталонным {IMAGE_SIZE}"