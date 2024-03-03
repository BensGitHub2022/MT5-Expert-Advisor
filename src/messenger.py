# NOTE: For websocket test
from src.interfaces import IMessenger
import threading
import websockets
import websockets.sync
import websockets.sync.server

class Messenger(IMessenger):
    
    
    def __init__(self) -> None:
        self.sem = threading.Semaphore()
        self.lock = threading.Lock()
        self.queue = list()
        self.thread = threading.Thread(target=self.server_thread_proc)
        self.cancelled = False

    def queue_message(self, message: str) -> bool:
        self.lock.acquire()
        self.queue.append(message)
        self.sem.release()
        self.lock.release()
        return True

    def get_message(self) -> str:
        self.sem.acquire()
        message = ""
        self.lock.acquire()
        if (self.queue != []):
            message = self.queue.pop(0)
        self.lock.release()
        return message
    
    def trade_bot_service(self, websocket):
        while (not self.cancelled):
            message = self.get_message()
            if (message != ""):
                websocket.send(message)

    def server_thread_proc(self):
        self.server = websockets.sync.server.serve(self.trade_bot_service, "localhost", 5678)
        self.server.serve_forever()

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.socket.close()
        self.cancelled = True
        self.thread.join()
        