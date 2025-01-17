import init_path
from dependency_injector import containers, providers
from env_configurator_reader import EnvConfiguratorReader
from rabbitmq.rabbitmq_client import RabbitMQClient
from env_configurator_reader import EnvConfiguratorReader
from rabbitmq.rabbitmq_client import RabbitMQClient
from video_capture_factory import VideoCaptureFactory
from image_handler import ImageHandler
from video_capture_service import VideoCaptureService
from video_capture_svc import VideoCaptureSvc

class ApplicationContainer(containers.DeclarativeContainer):
    # Конфигуратор
    configurator = providers.Factory(EnvConfiguratorReader)
    
    # Зависимости
    configuration = providers.Callable(lambda: ApplicationContainer.configurator().read())
    rabbitmq_client = providers.Factory(RabbitMQClient, configuration=configuration)
    
    # Провайдер для фабрики VideoCaptureFactory
    video_capture_factory = providers.Factory(VideoCaptureFactory)
    
    # Провайдер для создания объекта capture
    capture = providers.Factory(
        lambda factory, config: factory.create(config),
        video_capture_factory,
        configuration,
    )
    
    image_handler = providers.Factory(ImageHandler)
    
    video_capture_service = providers.Factory(
        VideoCaptureService,
        configuration=configuration,
        rabbitmq_client=rabbitmq_client,
        capture=capture,
        image_handler=image_handler
    )
    
    video_capture_svc = providers.Factory(VideoCaptureSvc)