from capture import Capture

class CameraCapture(Capture):
    """
    A class for capturing events from a camera in a separate thread.

    Inherits from the `Capture` base class and provides methods to start and 
    stop the capture process. The capture process runs in a separate thread 
    and periodically notifies an event.

    Attributes:
        __starting (bool): A flag indicating whether the capture process is running.
        __thread (threading.Thread): The thread running the capture process.

    Methods:
        start():
            Starts the capture process in a separate thread.
        _run_capture():
            Internal method that implements the capture loop.
        stop():
            Stops the capture process and waits for the thread to finish.
    """
    
    def __init__(self, settings=None):
        super().__init__(settings)

    def _handle_capture(self):
        print("Capture from camera")
        
        return None