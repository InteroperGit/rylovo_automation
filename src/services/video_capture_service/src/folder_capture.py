from capture import Capture
import os
import cv2

class FolderCapture(Capture):
    def __init__(self, settings=None):
        super().__init__(settings)
        
        source_folder = settings["source_folder"]
        
        if not isinstance(source_folder, str):
            raise ValueError("Source folder must be a defined")
        
        if not os.path.exists(source_folder):
            raise ValueError(f"Source folder [{source_folder}] is not exists.")
        
        if not os.path.isdir(source_folder):
            raise ValueError(f"Source folder [{source_folder}] is not a directory.")
        
    def __image_generator(self, directory):
        # Получаем список файлов в директории
        files = os.listdir(directory)
        image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

        if not image_files:
            print("В директории нет изображений.")
            return
        
        for image_file in image_files:
            print(image_file)
            image_path = os.path.join(directory, image_file)
            try:
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Не удалось загрузить файл {image_file}. Пропуск.")
                    continue
                yield image
            except Exception as e:
                print(f"Ошибка при загрузке {image_file}: {e}")
        
    def _handle_capture(self):
        print(self._settings)
        
        for image in self.__image_generator(self._settings["source_folder"]):
            yield image