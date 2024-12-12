from camera_capture import CameraCapture
from folder_capture import FolderCapture
import os
import pika
import cv2
import base64
import json
import signal
import sys
import time

SLEEP_INTERVAL = 5

class CaptureService:
    def __init_capture(self):
        try:
            # e:\korayzma\images\saved\defects
            # os.getenv("SOURCE_FOLDER")
            settings = {
                "source_folder": os.getenv("SOURCE_FOLDER")
            }
            
            self._capture = FolderCapture(settings)
            
            return True
        except:
            return False
    
    def __init_rabbitmq(self):
        attempts = 0
        max_attempts = int(os.getenv("RABBITMQ_MAX_CONNECTION_ATTEMPTS"))  # Максимальное количество попыток подключения
        
        try:
            user = os.getenv("RABBITMQ_USER")
            password = os.getenv("RABBITMQ_PASSWORD")
            credentials = pika.PlainCredentials(user, password)
            rabbitmq_host = os.getenv("RABBITMQ_HOST")
            self._QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME")
            # Инициализация подключения
            print(f"Try to connect to RabbitMQ server: {rabbitmq_host} with credentials: {user}:{password}")
            
            while attempts < max_attempts:
                try:
                    print(f"Try to connect to RabbitMQ server: {rabbitmq_host}. Attempt: [{attempts}]")
                    self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
                    print("RabbitMQ. Connection established")
                    break
                except pika.exceptions.AMQPConnectionError as e:
                    print(f"RabbitMQ. Failed to connect. Attempt: {attempts + 1}/{max_attempts}: {e}")
                    time.sleep(SLEEP_INTERVAL)  # Задержка перед повторной попыткой
                    attempts += 1
                    
            if self._connection is None:
                raise Exception(f"Failed to connect to RabbitMQ after {max_attempts} attempts.")
                
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self._QUEUE_NAME, durable=True)
            print(f"RabbitMQ. Open queue: [{self._QUEUE_NAME}]")

            return True
        except Exception as e:
            print(f"RabbitMQ. Connection error: {e}")
            return False
        
    def __init__(self):
        capture_ready = self.__init_capture()
        rabbitmq_ready = self.__init_rabbitmq()
        self._ready = capture_ready and rabbitmq_ready
        self._started = False
        
    def handler(self, image):
        print(f"Получено изображение размером: {image.shape}")
        _, buffer = cv2.imencode('.jpg', image)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        
        message = {
            "timestamp": "2024-12-08T12:00:00Z",
            "camera_id": "CAM123",
            "image": encoded_image
        }
        
        self._channel.basic_publish(
            exchange='',
            routing_key=self._QUEUE_NAME,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # Сохранение сообщения на диск
            )
        )
    
    def start(self):
        if not self._started and self._ready:
            self._capture.subscribe(self.handler)
            self._capture.start()
            print("Capture service was successfully started")
        
    def stop(self):
        if self._started:
            if not self._capture is None:
                self._capture.unsubscribe(self.handler)
                self._capture.stop()
                print("Capture service was successfully stopped")
            
            if not self._connection is None:
                self._connection.close()

def signal_handler(framse, sig):
    print("Получен сигнал остановки. Завершаем работу...")
    service.stop()
    sys.exit(0)

if __name__ == "__main__":
    service = CaptureService()
    service.start()
    # Настроим обработку сигнала SIGINT (например, Ctrl+C) для корректного завершения работы
    signal.signal(signal.SIGINT, signal_handler)

    # Ожидаем сигналов ОС, служба будет работать, пока не получит сигнал
    print("Служба работает. Нажмите Ctrl+C для выхода.")

    while True:
        time.sleep(1)  # Спим 1 секунду, не давая CPU простаивать, и ждем сигналов
   