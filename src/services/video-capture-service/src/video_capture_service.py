class VideoCaptureService:
    def __init__(self, configuration, rabbitmq_client, capture, image_handler):
        self.__configuration = configuration
        self.__exchange_name = self.__configuration.get("rabbitmq_exchange_name")
        self.__rabbitmq_client = rabbitmq_client
        self.__capture = capture
        self.__image_handler = image_handler
        self.__started = False
        
    def __handler(self, image):
        json_message = self.__image_handler.handle(image)
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
