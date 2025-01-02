import pika
import os
import json
import base64
import cv2
import time
import numpy as np
from datetime import datetime

SLEEP_INTERVAL = 5

class ImageLoggingService:
    def __read_data(self):
        max_attempts = int(os.getenv("RABBITMQ_MAX_CONNECTION_ATTEMPTS"))  # Максимальное количество попыток подключения
        user = os.getenv("RABBITMQ_USER")
        password = os.getenv("RABBITMQ_PASSWORD")
        rabbitmq_host = os.getenv("RABBITMQ_HOST")
        exchange_name = os.getenv("RABBITMQ_EXCHNAGE_NAME")
        root_folder = os.getenv("IMAGE_ROOT_FOLDER")
        
        return {
            "max_attempts": max_attempts,
            "user": user,
            "password": password,
            "rabbitmq_host": rabbitmq_host,
            "exchange_name": exchange_name,
            "root_folder": root_folder
        }
    
    def __try_to_connect(self, max_attempts, rabbitmq_host, credentials):
        attempts = 0
        
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
    
    def __init_rabbitmq(self):
        data = self.__read_data()
        
        try:
            credentials = pika.PlainCredentials(data["user"], data["password"])
            self._EXCHANGE_NAME = data["exchange_name"]
            self._ROOT_FOLDER = data["root_folder"]
            
            # Инициализация подключения
            print(f"Try to connect to RabbitMQ server: {data["rabbitmq_host"]} with credentials: {data["user"]}:{data["password"]}")
            self.__try_to_connect(data["max_attempts"], data["rabbitmq_host"], credentials)
                    
            if self._connection is None:
                raise Exception(f"Failed to connect to RabbitMQ after {data["max_attempts"]} attempts.")
                
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
        
    def __parse_body(self, body):
        # Распаковка JSON-сообщения
        message = json.loads(body)
        timestamp = message.get("timestamp")
        camera_id = message.get("camera_id")
        encoded_image = message.get("image")
        
        return timestamp, camera_id, encoded_image
    
    def __decode_image(self, encoded_image):
        # Декодирование изображения
        image_data = base64.b64decode(encoded_image)
        np_image = np.frombuffer(image_data, dtype=np.uint8)
        return cv2.imdecode(np_image, cv2.IMREAD_COLOR)
           
    def __save_image(self, image):
        # Сохраняем изображение
        root_folder = self._ROOT_FOLDER
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d/%H")
        ms = f"{current_datetime.microsecond // 1000:03d}"
        formatted_datetime = f"{current_datetime.strftime('%Y%m%d_%H%M%S')}_{ms}"
        
        # Формируем путь к папке
        save_path = os.path.join(root_folder, formatted_date)
        
        # Создаём директории, если они ещё не существуют
        os.makedirs(save_path, exist_ok=True)
        
        # Формируем имя файла по шаблону
        file_name = f"image_{formatted_datetime}.jpg"
        full_path = os.path.join(save_path, file_name)
        
        success = cv2.imwrite(full_path, image)
        
        # Сохраняем изображение
        return success, full_path
           
    def __callback(self, ch, method, properties, body):
        try:
            timestamp, camera_id, encoded_image = self.__parse_body(body)
            image = self.__decode_image(encoded_image)

            # Вывод информации
            print(f"Получено изображение от камеры {camera_id} с timestamp: {timestamp}")
            print(f"Размер изображения: {image.shape}")
            
            save_successed, full_path = self.__save_image(image)
            
            if save_successed:
                print(f"Изображение успешно сохранено по пути: {full_path}")
            else:
                print(f"Ошибка при сохранении изображения.")
            
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