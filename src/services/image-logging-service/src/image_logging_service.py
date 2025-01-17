class ImageLoggingService:
    """
    Сервис для получения изображений из RabbitMQ, декодирования, обработки и сохранения их в указанную папку.

    Этот класс:
    - Читает конфигурацию из среды (EnvConfiguratorReader).
    - Устанавливает соединение с RabbitMQ для получения изображений.
    - Использует декодер для обработки изображений.
    - Сохраняет декодированные изображения на диск.
    """
    
    def __init__(self, rabbitmq_client, image_saver, image_decoder):
        """
        Инициализация сервиса.
        
        Создает экземпляры для:
        - Чтения конфигурации.
        - Работы с RabbitMQ.
        - Сохранения изображений.
        - Декодирования изображений.
        """
        self.__rabbitmq_client = rabbitmq_client
        self.__image_saver = image_saver
        self.__image_decoder = image_decoder
        self._started = False

    def __callback(self, ch, method, properties, body):
        """
        Обрабатывает сообщение, полученное из RabbitMQ.

        - Декодирует изображение.
        - Выводит информацию о полученном изображении.
        - Сохраняет изображение в заданную папку.
        - Подтверждает или отклоняет сообщение в зависимости от результата.

        Args:
            ch: Канал RabbitMQ.
            method: Метаданные сообщения.
            properties: Свойства сообщения.
            body: Содержимое сообщения (закодированное изображение).
        """
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
        """
        Запускает сервис.
        
        - Устанавливает соединение с RabbitMQ.
        - Начинает получение сообщений через колбэк.
        """
        if not self._started:
            try:
                self.__rabbitmq_client.connect()
                self.__rabbitmq_client.start_consuming(self.__callback)
                print("ImageLoggingService was successfully started")
            except Exception as ex:
                print(f"Failed to start ImageLoggingService: [{ex}]")

    def stop(self):
        """
        Останавливает сервис.

        - Завершает обработку сообщений из RabbitMQ.
        - Закрывает соединение с RabbitMQ.
        """
        if self._started:
            if not self._connection is None:
                try:
                    self.__rabbitmq_client.stop_consuming()
                    print("ImageLoggingService was successfully stopped")
                except Exception as ex:
                    print(f"Failed to stop ImageLoggingService: [{ex}]")