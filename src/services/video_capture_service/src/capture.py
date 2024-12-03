from event import Event
import time
import threading

class Capture:
    def __init__(self, settings=None):
        self._event = Event()
        self._settings = settings
        self.__starting = False
        self.__thread = None
    
    def subscribe(self, handler):
        self._event.subscribe(handler)
    
    def unsubscribe(self, handler):
        self._event.unsubscribe(handler)
        
    def _handle_capture(self):
        pass
        
    def _run_capture(self):
        gen = self._handle_capture()
        
        while self.__starting:
            try:
                time.sleep(1)
                image = next(gen)
                self._event.notify(image)
            except Exception as e:
                print(f"Error: {e}")
                
    def start(self):
        if self.__starting:
           return 
       
        self.__starting = True
        self.__thread = threading.Thread(target=self._run_capture)
        self.__thread.start()
    
    def stop(self):
        self.__starting = False
        
        if self.__thread is not None:
            self.__thread.join()