import sys
import signal
import time
from image_logging_service import ImageLoggingService

def signal_handler(framse, sig):
    print("Получен сигнал остановки. Завершаем работу...")
    service.stop()
    sys.exit(0)

if __name__ == "__main__":
    try:
        service = ImageLoggingService()
    except Exception as e:
        print(f"Image logging service. Error: {e}")
        exit(1)
        
    service.start()
    # Настроим обработку сигнала SIGINT (например, Ctrl+C) для корректного завершения работы
    signal.signal(signal.SIGINT, signal_handler)

    # Ожидаем сигналов ОС, служба будет работать, пока не получит сигнал
    print("Служба работает. Нажмите Ctrl+C для выхода.")

    while True:
        time.sleep(1)  # Спим 1 секунду, не давая CPU простаивать, и ждем сигналов