import init_path
from env_configurator_reader import EnvConfiguratorReader
from rabbitmq.rabbitmq_client import RabbitMQClient
from folder_image_saver import FolderImageSaver
from image_decoder import ImageDecoder

class ImageLoggingService:
    def __init__(self):
        configurator = EnvConfiguratorReader()
        self.__configuration = configurator.read()
        self.__rabbitmq_client = RabbitMQClient(self.__configuration)
        self.__image_saver = FolderImageSaver(self.__configuration)
        self.__image_decoder = ImageDecoder()
        self._started = False

    def __callback(self, ch, method, properties, body):
        try:
            timestamp, camera_id, image = self.__image_decoder.decode_image(body)

            # Вывод информации
            print(f"Получено изображение от камеры {camera_id} с timestamp: {timestamp}")
            print(f"Размер изображения: {image.shape}")
            
            save_successed, full_path = self.__image_saver.save(image)
            
            if save_successed:
                print(f"Изображение успешно сохранено по пути: {full_path}")
            else:
                print(f"Ошибка при сохранении изображения.")
            
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")
            # Не подтверждаем сообщение, чтобы оно осталось в очереди
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def start(self):
        if not self._started:
            try:
                self.__rabbitmq_client.connect()
                self.__rabbitmq_client.start_consuming(self.__callback)
                print("VideoLoggingService was successfully started")
            except Exception as ex:
                print(f"Failed to start VideoLoggingService: [{ex}]")

    def stop(self):
        if self._started:
            if not self._connection is None:
                try:
                    self.__rabbitmq_client.stop_consuming()
                    print("VideoLoggingService was successfully stopped")
                except Exception as ex:
                    print(f"Failed to stop VideoLoggingService: [{ex}]")