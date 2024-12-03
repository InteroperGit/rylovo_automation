class Event:
    def __init__(self):
        self.__subscribers = []
        
    def subscribe(self, handler) -> None:
        self.__subscribers.append(handler)
        
    def unsubscribe(self, handler) -> None:
       self.__subscribers.remove(handler)
       
    def notify(self, *args, **kwargs) -> None:
        for handler in self.__subscribers:
            handler(*args, **kwargs)