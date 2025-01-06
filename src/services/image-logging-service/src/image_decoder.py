import json
import base64
import numpy as np
import cv2

class ImageDecoder:
    def __parse_body(self, body):
        # Распаковка JSON-сообщения
        message = json.loads(body)
        timestamp = message.get("timestamp")
        camera_id = message.get("camera_id")
        encoded_image = message.get("image")
        
        return timestamp, camera_id, encoded_image
    
    def decode_image(self, body):
        timestamp, camera_id, encoded_image = self.__parse_body(body)
        
        # Декодирование изображения
        image_data = base64.b64decode(encoded_image)
        np_image = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        
        return timestamp, camera_id, image