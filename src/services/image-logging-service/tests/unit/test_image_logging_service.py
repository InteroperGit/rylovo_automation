import pytest
from app_container import ApplicationContainer

# Фикстура для контейнера
@pytest.fixture
def container():
    return ApplicationContainer()

def test_image_logging_service_start(container):
    # Мокаем метод start_consuming для RabbitMQClient
    mock_rabbitmq_client = container.rabbitmq_client()
    mock_rabbitmq_client.connect.return_value = None
    mock_rabbitmq_client.start_consuming.return_value = None
    
    # Мокаем другие компоненты
    mock_image_saver = container.image_saver()
    mock_image_decoder = container.image_decoder()
    
    # Создаем экземпляр ImageLoggingService с использованием мока и конфигурации
    svc = container.image_logging_service()
    
    # Проверяем, что сервис запускается и не вызывает исключений
    try:
        svc.start()
    except Exception as e:
        pytest.fail(f"Start method raised an exception: {e}")
        
    # Проверяем вызовы моков
    mock_rabbitmq_client.connect.assert_called_once()
    mock_rabbitmq_client.start_consuming.assert_called_once()
    
    # Теперь проверяем, что сервис останавливается без исключений
    try:
        svc.stop()
    except Exception as e:
        pytest.fail(f"Stop method raised an exception: {e}")