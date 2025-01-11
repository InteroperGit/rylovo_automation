import cv2
import numpy as np
import base64
import time
import json

class ImageHandler:
    def handle(self, image: np.ndarray) -> str:
        _, buffer = cv2.imencode('.jpg', image)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        message = {
            "timestamp": timestamp,
            "camera_id": "CAM123",
            "image": encoded_image
        }
        return json.dumps(message)