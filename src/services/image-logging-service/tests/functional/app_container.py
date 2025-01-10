from dependency_injector import containers, providers
from unittest.mock import Mock
from image_logging_service import ImageLoggingService
from folder_image_saver import FolderImageSaver
from rabbitmq.rabbitmq_client import RabbitMQClient
from image_decoder import ImageDecoder

class ApplicationContainer(containers.DeclarativeContainer):
    configuration = providers.Singleton(lambda: {
        "rabbitmq_connection_max_attempts": "5",
        "rabbitmq_user": "user",
        "rabbitmq_password": "password",
        "rabbitmq_host": "amqp://localhost",
        "rabbitmq_exchange_name": "rabbitmq_exchange",
        "image_save_root_folder": "/tmp"
    })
    
    # Мокаем зависимости
    rabbitmq_client = providers.Singleton(Mock(spec=RabbitMQClient))
    image_saver = providers.Singleton(Mock(spec=FolderImageSaver))
    image_decoder = providers.Singleton(Mock(spec=ImageDecoder))

    # Передаем все зависимости в ImageLoggingService
    image_logging_service = providers.Factory(
        ImageLoggingService,
        rabbitmq_client=rabbitmq_client,
        image_saver=image_saver,
        image_decoder=image_decoder,
    )
    