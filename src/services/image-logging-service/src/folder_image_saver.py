import os
import cv2
from datetime import datetime

class FolderImageSaver:
    def __init__(self, configuration):
        self.__image_save_root_folder = configuration.get("image_save_root_folder")
        
    def save(self, image):
        # Сохраняем изображение
        root_folder = self.__image_save_root_folder
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d/%H")
        ms = f"{current_datetime.microsecond // 1000:03d}"
        formatted_datetime = f"{current_datetime.strftime('%Y%m%d_%H%M%S')}_{ms}"
        
        # Формируем путь к папке
        save_path = os.path.join(root_folder, formatted_date)
        
        # Создаём директории, если они ещё не существуют
        os.makedirs(save_path, exist_ok=True)
        
        # Формируем имя файла по шаблону
        file_name = f"image_{formatted_datetime}.jpg"
        full_path = os.path.join(save_path, file_name)
        
        success = cv2.imwrite(full_path, image)
        
        # Сохраняем изображение
        return success, full_path