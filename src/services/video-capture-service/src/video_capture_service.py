import init_path
import cv2
import base64
import json
import time
from env_configurator_reader import EnvConfiguratorReader
from rabbitmq.rabbitmq_client import RabbitMQClient
from video_capture_factory import VideoCaptureFactory

class VideoCaptureService:
    def __init__(self):
        configurator = EnvConfiguratorReader()
        self.__configuration = configurator.read()
        self.__exchange_name = self.__configuration.get("rabbitmq_exchange_name")
        self.__rabbitmq_client = RabbitMQClient(self.__configuration)
        self.__capture = VideoCaptureFactory().create(self.__configuration)
        self.__started = False
        
    def __handler(self, image):
        _, buffer = cv2.imencode('.jpg', image)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        message = {
            "timestamp": timestamp,
            "camera_id": "CAM123",
            "image": encoded_image
        }
        json_message = json.dumps(message)
        
        self.__rabbitmq_client.send(self.__exchange_name, json_message)
        
        print("Изображение было успешно отправлено")
    
    def start(self):
        if self.__started:
            return
        
        self.__rabbitmq_client.connect()
        self.__capture.subscribe(self.__handler)
        self.__capture.start()
        self.__started = True
        print("Video capture service was successfully started")
        
    def stop(self):
        if not self.__started:
            return
        
        try:
            if not self.__capture is None:
                self._capture.unsubscribe(self.__handler)
                self._capture.stop()
                print("Video capture service was successfully stopped")
            
            if not self._connection is None:
                self._connection.close()
                print("RabbitMQ connection was successfully closed")
        finally:
            self.__started = False
