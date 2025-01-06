import os

class EnvConfiguratorReader:
    def read(self):
        connection_max_attempts = int(os.getenv("RABBITMQ_MAX_CONNECTION_ATTEMPTS"))  # Максимальное количество попыток подключения
        rabbitmq_user = os.getenv("RABBITMQ_USER")
        rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")
        rabbitmq_host = os.getenv("RABBITMQ_HOST")
        rabbitmq_exchange_name = os.getenv("RABBITMQ_EXCHNAGE_NAME")
        image_save_root_folder = os.getenv("IMAGE_SAVE_ROOT_FOLDER")
        
        return {
            "rabbitmq_connection_max_attempts": connection_max_attempts,
            "rabbitmq_user": rabbitmq_user,
            "rabbitmq_password": rabbitmq_password,
            "rabbitmq_host": rabbitmq_host,
            "rabbitmq_exchange_name": rabbitmq_exchange_name,
            "image_save_root_folder": image_save_root_folder
        }