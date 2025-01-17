import sys
import signal
import time
import threading
from app_container import ApplicationContainer

def signal_handler(framse, sig):
    try:
        print("Получен сигнал остановки. Завершаем работу...")
        service.stop()
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка при останове службы: [{e}]")
        sys.exit(1)
    
if __name__ == "__main__":
    try:
        container = ApplicationContainer()
        service = container.image_logging_service()
        svc = container.image_logging_svc()
        
        def start_service():
            service.start()
            
        def start_svc():
            svc.start()
            
        service_thread = threading.Thread(target=start_service)
        service_thread.start()
        
        service_thread = threading.Thread(target=start_svc)
        service_thread.start()
        
        # Настроим обработку сигнала SIGINT (например, Ctrl+C) для корректного завершения работы
        signal.signal(signal.SIGINT, signal_handler)

        # Ожидаем сигналов ОС, служба будет работать, пока не получит сигнал
        print("Служба работает. Нажмите Ctrl+C для выхода.")

        while True:
            time.sleep(1)  # Спим 1 секунду, не давая CPU простаивать, и ждем сигналов
    except Exception as e:
        print(f"Image logging service. Error: {e}")
        exit(1)