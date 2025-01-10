import init_path
from dependency_injector import containers, providers
from env_configurator_reader import EnvConfiguratorReader
from rabbitmq.rabbitmq_client import RabbitMQClient
from folder_image_saver import FolderImageSaver
from image_decoder import ImageDecoder
from image_logging_service import ImageLoggingService

class ApplicationContainer(containers.DeclarativeContainer):
    # Конфигуратор
    configurator = providers.Factory(EnvConfiguratorReader)
    
    # Зависимости
    configuration = providers.Callable(lambda: ApplicationContainer.configurator().read())
    rabbitmq_client = providers.Factory(RabbitMQClient, configuration=configuration)
    image_saver = providers.Factory(FolderImageSaver, configuration=configuration)
    image_decoder = providers.Factory(ImageDecoder)
    
    image_logging_service = providers.Factory(
        ImageLoggingService,
        rabbitmq_client=rabbitmq_client,
        image_saver=image_saver,
        image_decoder=image_decoder
    )