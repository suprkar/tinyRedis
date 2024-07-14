import threading
import time
import resp

class AOF:
    def __init__(self, path):
        self.path = path
        self.file = open(path, 'a+b')
        self.lock = threading.Lock()

        # Start a thread to sync AOF to disk every second
        threading.Thread(target=self.sync_to_disk, daemon=True).start()

    def sync_to_disk(self):
        while True:
            time.sleep(1)
            with self.lock:
                self.file.flush()

    def close(self):
        with self.lock:
            self.file.close()

    def write(self, value):
        with self.lock:
            self.file.write(resp.marshal(value))
            self.file.flush()

    def read(self, fn):
        with self.lock:
            self.file.seek(0)
            data = self.file.read()
            while data:
                value, data = resp.read(data)
                fn(value)

# Rest of aof.py remains the same
