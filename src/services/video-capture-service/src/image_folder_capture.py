from capture import Capture
import os
import cv2
from typing import Dict

class ImageFolderCapture(Capture):
    def __init_source_folder(self):
        image_source_folder = self._configuration["image_source_folder"]
        
        if not isinstance(image_source_folder, str):
            raise ValueError("Source folder must be a defined")
        
        if not os.path.exists(image_source_folder):
            raise ValueError(f"Source folder [{image_source_folder}] is not exists.")
        
        if not os.path.isdir(image_source_folder):
            raise ValueError(f"Source folder [{image_source_folder}] is not a directory.")
        
        self.__image_source_folder = image_source_folder
    
    def __init__(self, configuration: Dict[str, str] = None) -> None:
        super().__init__(configuration)
        self.__init_source_folder()
        
    def __image_generator(self, image_folder):
        # Получаем список файлов в директории
        files = os.listdir(image_folder)
        image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

        if not image_files:
            print("В директории нет изображений.")
            return
        
        for image_file in image_files:
            print(f"Считано изображение: {image_file}")
            image_path = os.path.join(image_folder, image_file)
            try:
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Не удалось загрузить файл {image_file}. Пропуск.")
                    continue
                yield image
            except Exception as e:
                print(f"Ошибка при загрузке {image_file}: {e}")
        
    def _handle_capture(self):
        for image in self.__image_generator(self.__image_source_folder):
            yield image