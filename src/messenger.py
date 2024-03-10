# NOTE: For websocket test
from src.interfaces import IMessenger
import threading
import websockets
import websockets.sync
import websockets.sync.server
import logging

HOST = "localhost"
PORT = 5678

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)

class Messenger(IMessenger):    
    
    def __init__(self) -> None:
        self.sem = threading.Semaphore()
        self.lock = threading.Lock()
        self.queue = list()
        self.thread = threading.Thread(target=self.server_thread_proc)
        self.cancelled = False
        self.logger = logging.getLogger(__name__)

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
    
    def trade_bot_service(self, server_connection: websockets.server.ServerConnection):
        self.server_connection = server_connection
        while (not self.cancelled):
            message = self.get_message()
            if (message != ""):
                self.server_connection.send(message)
            received_msg = server_connection.recv()
            print(received_msg)
        self.server_connection.close()
        
    def server_thread_proc(self):
        self.websocket_server = websockets.sync.server.serve(self.trade_bot_service, HOST, PORT, open_timeout=None, close_timeout=None, logger=self.logger)
        self.websocket_server.serve_forever()

    def start(self):
        print("Serving websocket on " + HOST + " at " + str(PORT) + ".")
        self.thread.start()

    def stop(self):
        self.server_connection.close()
        self.cancelled = True
        self.thread.join()
        