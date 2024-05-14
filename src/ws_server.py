# NOTE: For websocket test
from src.interfaces import IMessenger

import threading
import websockets
import websockets.sync.server
import logging

HOST = "localhost"
PORT = 5678
'''
logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)'''

class ConnectionInfo():

    def __init__(self, connection) -> None:
        self.connection = connection
        self.sem = threading.Semaphore(0)

    def signal(self):
        self.sem.release()

class Messenger(IMessenger):    
    
    def __init__(self) -> None:
        self.sem = threading.Semaphore()
        self.lock = threading.Lock()
        self.queue = list()
        self.connection_list = list()
        self.connection_list_lock = threading.Lock()
        self.thread = threading.Thread(target=self.thread_proc)
        self.cancelled = False

    def start(self):
        self.thread.start()

    def stop(self):
        self.cancelled = True
        for connection_info in self.connection_list:
            connection_info.connection.close()
            connection_info.signal()
        self.sem.release()
        self.thread.join()

    def queue_message(self, message: str) -> bool:
        self.lock.acquire()
        self.queue.append(message)
        self.sem.release()
        self.lock.release()
        return True

    def get_message(self) -> str:
        self.sem.acquire()
        message = ""
        if (self.cancelled):
            return message
        self.lock.acquire()
        if (self.queue != []):
            message = self.queue.pop(0)
        self.lock.release()
        return message
    
    def server_connection(self, server_connection: websockets.server.ServerConnection):
        print(threading.get_native_id())
        connection_info = ConnectionInfo(server_connection)
        self.connection_list_lock.acquire()
        self.connection_list.append(connection_info)
        self.connection_list_lock.release()
        while (not self.cancelled):
            connection_info.sem.acquire()
            print("Terminating!")
            break
    
    def thread_proc(self):
        while (not self.cancelled):
            message = self.get_message()
            if (message == ""):
                continue

            self.connection_list_lock.acquire()
            connection_list_copy = self.connection_list.copy()
            self.connection_list_lock.release()
            for connection_info in connection_list_copy:
                try:
                    connection_info.connection.send(message)
                except Exception as e:
                    self.remove_connection(connection_info)
                    print(e.args)

    def remove_connection(self, connection_info_to_remove):
        self.connection_list_lock.acquire()
        index = 0
        for connection_info in self.connection_list:
            if (connection_info.connection == connection_info_to_remove.connection):
                self.connection_list.pop(index)
                connection_info.signal()
                break
            index += 1
        self.connection_list_lock.release()

class TradeBotWebsocketServer():
    def __init__(self, messenger: Messenger) -> None:
        self.thread = threading.Thread(target=self.server_thread_proc)
        self.messenger = messenger

    def server_thread_proc(self): 
        self.websocket_server = websockets.sync.server.serve(self.messenger.server_connection, HOST, PORT, open_timeout=None, close_timeout=None)
        self.websocket_server.serve_forever()

    def start(self):
        print("Serving websocket on " + HOST + " at " + str(PORT) + ".")
        self.thread.start()

    def stop(self):
        print("Ending websocket service!")
        self.websocket_server.shutdown()
        self.thread.join()       