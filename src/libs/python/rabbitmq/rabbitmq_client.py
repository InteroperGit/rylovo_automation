import pika
import time
from typing import Dict, Callable

SLEEP_INTERVAL = 5

class RabbitMQClient:
    def __init__(self, configuration: Dict[str, str]) -> None:
        self.__configuration = configuration
        self.__connected = False
        self.__started = False
        
    def __try_to_connect(self):
        config = self.__configuration
        
        connection_max_attempts = config.get("rabbitmq_connection_max_attempts")
        rabbitmq_host = config.get('rabbitmq_host')
        rabbitmq_user = config.get('rabbitmq_user')
        rabbitmq_password = config.get('rabbitmq_password')
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        attempts = 0
        
        while attempts < connection_max_attempts:
            try:
                print(f"Try to connect to RabbitMQ server: {rabbitmq_host}. Attempt: [{attempts}]")
                self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
                print("RabbitMQ. Connection established")
                break
            except pika.exceptions.AMQPConnectionError as e:
                print(f"RabbitMQ. Failed to connect. Attempt: {attempts + 1}/{connection_max_attempts}: {e}")
                time.sleep(SLEEP_INTERVAL)  # Задержка перед повторной попыткой
                attempts += 1
        
    def __init_consuming(self, callback: Callable[[], None]) -> None:
        config = self.__configuration
        rabbitmq_exchange_name = config.get("rabbitmq_exchange_name")
        
        # Создаем уникальную очередь для каждого получателя
        result = self.__channel.queue_declare(queue='', exclusive=True)
        self.__queue_name = result.method.queue
        
        # Привязываем очередь к обменнику
        self.__channel.queue_bind(exchange=rabbitmq_exchange_name, queue= self.__queue_name)
        self.__channel.basic_consume(queue= self.__queue_name, on_message_callback=callback, auto_ack=True)
        
        print(f"RabbitMQ. Open queue: [{ self.__queue_name}]")
      
    def connect(self):
        config = self.__configuration
        
        connection_max_attempts = config.get("rabbitmq_connection_max_attempts")
        rabbitmq_host = config.get('rabbitmq_host')
        rabbitmq_user = config.get('rabbitmq_user')
        rabbitmq_password = config.get('rabbitmq_password')
        rabbitmq_exchange_name = config.get("rabbitmq_exchange_name")
        
        # Инициализация подключения
        print(f"Try to connect to RabbitMQ server: {rabbitmq_host} with credentials: {rabbitmq_user}:{rabbitmq_password}")
        self.__try_to_connect()
                
        if self.__connection is None:
            raise Exception(f"Failed to connect to RabbitMQ after {connection_max_attempts} attempts.")
            
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(exchange=rabbitmq_exchange_name, exchange_type='fanout')
        print(f"RabbitMQ. Open exchange: [{rabbitmq_exchange_name}]")
        
        self.__connected = True
        
    def start_consuming(self, callback: Callable[[], None]) -> None:
        if not self.__connected:
            return
        
        if self.__started:
            return
        
        self.__init_consuming(callback)
        self.__channel.start_consuming()
        self.__started = True
            
    def stop_consuming(self) -> None:
        if not self.__started or not self.__connected:
            return
        
        try:
            self.__channel.stop_consuming()
            self.__connection.close()
        finally:
            self.__started = False
            
    def send(self, exchange_name, message) -> None:
        if self.__channel is None:
            return
        
        self.__channel.basic_publish(
            exchange=exchange_name,
            routing_key="",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # Сохранение сообщения на диск
            )
        )