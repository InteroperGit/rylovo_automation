import sys
import signal
import time
import pika
import os
import json
import base64
import cv2
import numpy as np

SLEEP_INTERVAL = 5

class ImageLoggingService:
    def __init_rabbitmq(self):
        attempts = 0
        max_attempts = int(os.getenv("RABBITMQ_MAX_CONNECTION_ATTEMPTS"))  # Максимальное количество попыток подключения
        
        try:
            user = os.getenv("RABBITMQ_USER")
            password = os.getenv("RABBITMQ_PASSWORD")
            credentials = pika.PlainCredentials(user, password)
            rabbitmq_host = os.getenv("RABBITMQ_HOST")
            self._EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHNAGE_NAME")
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
            self._channel.exchange_declare(exchange=self._EXCHANGE_NAME, exchange_type='fanout')
            print(f"RabbitMQ. Open exchange: [{self._EXCHANGE_NAME}]")
            
            # Создаем уникальную очередь для каждого получателя
            result = self._channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            
            # Привязываем очередь к обменнику
            self._channel.queue_bind(exchange=self._EXCHANGE_NAME, queue=queue_name)
            self._channel.basic_consume(queue=queue_name, on_message_callback=self.__callback, auto_ack=True)
            print(f"RabbitMQ. Open queue: [{queue_name}]")
            
            return True
        except Exception as e:
            print(f"RabbitMQ. Connection error: {e}")
            return False
        
    def __init__(self):
        rabbitmq_ready = self.__init_rabbitmq()
        self._ready = rabbitmq_ready
        self._started = False
        
    def __callback(self, ch, method, properties, body):
        try:
            # Распаковка JSON-сообщения
            message = json.loads(body)
            timestamp = message.get("timestamp")
            camera_id = message.get("camera_id")
            encoded_image = message.get("image")
            
            # Декодирование изображения
            image_data = base64.b64decode(encoded_image)
            np_image = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

            # Вывод информации
            print(f"Получено изображение от камеры {camera_id} с timestamp: {timestamp}")
            print(f"Размер изображения: {image.shape}")
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")
            # Не подтверждаем сообщение, чтобы оно осталось в очереди
            ch.basic_nack(delivery_tag=method.delivery_tag)
        
    def start(self):
        print(f"started = [{self._started}], ready = [{self._ready}]")
        
        if not self._started and self._ready:
            try:
                self._channel.start_consuming()
                print("VideoLoggingService was successfully started")
            except Exception as ex:
                print(f"Failed to start VideoLoggingService: [{ex}]")

    def stop(self):
        if self._started:
            if not self._connection is None:
                try:
                    self._channel.stop_consuming()
                    self._connection.close()
                    print("VideoLoggingService was successfully stopped")
                except Exception as ex:
                    print(f"Failed to stop VideoLoggingService: [{ex}]")
        
def signal_handler(framse, sig):
    print("Получен сигнал остановки. Завершаем работу...")
    service.stop()
    sys.exit(0)

if __name__ == "__main__":
    service = ImageLoggingService()
    service.start()
    # Настроим обработку сигнала SIGINT (например, Ctrl+C) для корректного завершения работы
    signal.signal(signal.SIGINT, signal_handler)

    # Ожидаем сигналов ОС, служба будет работать, пока не получит сигнал
    print("Служба работает. Нажмите Ctrl+C для выхода.")

    while True:
        time.sleep(1)  # Спим 1 секунду, не давая CPU простаивать, и ждем сигналов