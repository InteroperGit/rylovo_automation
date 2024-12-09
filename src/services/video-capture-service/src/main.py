from camera_capture import CameraCapture
from folder_capture import FolderCapture
import keyboard
import os

class CaptureService:
    def __init__(self):
        # e:\korayzma\images\saved\defects
        settings = {
            "source_folder": os.getenv("SOURCE_FOLDER")
        }
        
        self.capture = FolderCapture(settings)
    
    def handler(self, image):
        print(f"Получено изображение размером: {image.shape}")
    
    def start(self):
        self.capture.subscribe(self.handler)
        self.capture.start()
        
    def stop(self):
        self.capture.stop()
        self.capture.unsubscribe(self.handler)

if __name__ == "__main__":
    service = CaptureService()
    service.start()
    print("Нажмите любую клавишу для выхода")
    keyboard.read_event()
    service.stop()        