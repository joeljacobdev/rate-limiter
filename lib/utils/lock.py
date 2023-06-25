import threading


class LockManager:
    def __init__(self):
        self.global_lock = threading.Lock()
        self.locks = {}

    def get_lock(self, key):
        with self.global_lock:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
        lock = Lock(self.locks[key])
        return lock


class Lock:
    def __init__(self, lock: threading.Lock):
        self.lock = lock

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

