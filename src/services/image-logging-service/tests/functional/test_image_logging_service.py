import pytest
from app_container import ApplicationContainer
from unittest.mock import Mock

# Фикстура для контейнера
@pytest.fixture
def container():
    return ApplicationContainer()

def test_image_logging_service_load_image(container):
    # Настройка моков
    mock_rabbitmq_client = container.rabbitmq_client()
    mock_image_decoder = container.image_decoder()
    mock_image_saver = container.image_saver()
    
    # Фейковые данные для теста
    fake_body = b"fake_image_data"
    fake_timestamp = "2025-01-10T12:00:00Z"
    fake_camera_id = "camera_01"
    fake_image = Mock()  # Имитируем объект изображения
    fake_save_path = "/tmp/fake_image.jpg"
    
    # Настройка поведения моков
    mock_image_decoder.decode_image.return_value = (
        fake_timestamp, 
        fake_camera_id, 
        fake_image
    )
    
    mock_image_saver.save.return_value = (True, fake_save_path)
    
    # Создаем экземпляр сервиса
    svc = container.image_logging_service()
    
    # Имитируем вызов callback
    svc._ImageLoggingService__callback(
        ch=Mock(), 
        method=Mock(delivery_tag=1), 
        properties=Mock(), 
        body=fake_body
    )
    
    # Проверяем вызовы
    mock_image_decoder.decode_image.assert_called_once_with(fake_body)
    mock_image_saver.save.assert_called_once_with(fake_image)
    mock_rabbitmq_client.basic_nack.assert_not_called()  # Сообщение должно быть подтверждено