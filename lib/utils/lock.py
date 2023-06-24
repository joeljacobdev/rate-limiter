import threading


class LockManager:
    def __init__(self):
        self.global_lock = threading.Lock()
        self.locks = {}

    def get_lock(self, key, skip_lock=False):
        with self.global_lock:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
        return Lock(self.locks[key], skip_lock=skip_lock)


class Lock:
    def __init__(self, lock: threading.Lock, skip_lock: bool):
        self.lock = lock
        self.skip_lock = skip_lock

    def __enter__(self):
        if not self.skip_lock:
            self.lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.skip_lock:
            self.lock.release()

