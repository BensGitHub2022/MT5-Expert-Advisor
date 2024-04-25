import concurrent.futures
import queue
import threading

class PoolManager(object):
    pool : concurrent.futures.ThreadPoolExecutor
    pipeline: queue.Queue
    event: threading.Event

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.pool = concurrent.futures.ThreadPoolExecutor()
            cls.pipeline = queue.Queue(maxsize=10)
            cls.event = threading.Event()
            cls.instance = super(PoolManager, cls).__new__(cls)
        return cls.instance