import os

class EnvConfiguratorReader:
    def read(self):
        connection_max_attempts = int(os.getenv("RABBITMQ_MAX_CONNECTION_ATTEMPTS"))  # Максимальное количество попыток подключения
        rabbitmq_user = os.getenv("RABBITMQ_USER")
        rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")
        rabbitmq_host = os.getenv("RABBITMQ_HOST")
        rabbitmq_exchange_name = os.getenv("RABBITMQ_EXCHNAGE_NAME")
        video_capture_type = os.getenv("VIDEO_CAPTURE_TYPE")
        image_source_folder = os.getenv("IMAGE_SOURCE_FOLDER")
        
        return {
            "rabbitmq_connection_max_attempts": connection_max_attempts,
            "rabbitmq_user": rabbitmq_user,
            "rabbitmq_password": rabbitmq_password,
            "rabbitmq_host": rabbitmq_host,
            "rabbitmq_exchange_name": rabbitmq_exchange_name,
            "video_capture_type": video_capture_type,
            "image_source_folder": image_source_folder
        }