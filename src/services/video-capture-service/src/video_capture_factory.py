from typing import Dict
from capture import Capture
from camera_capture import CameraCapture
from image_folder_capture import ImageFolderCapture

class VideoCaptureFactory:
    def create(self, configuration: Dict[str, str]) -> Capture:
        capture_type = configuration.get("video_capture_type")
        
        if capture_type is None:
            raise ValueError("Video capture type must be an integer in range [0, 1]")
        
        capture_type = int(capture_type)
        capture = None
        
        if capture_type == 0:
            capture = CameraCapture(configuration)
        elif capture_type == 1:
            capture = ImageFolderCapture(configuration)    
        else:
            raise ValueError("Video capture type must be an integer in range [0, 1]")
            
        return capture           