from camera_capture import CameraCapture
from folder_capture import FolderCapture
import keyboard

class CaptureService:
    def __init__(self):
        settings = {
            "source_folder": f"e:\korayzma\images\saved\defects"
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