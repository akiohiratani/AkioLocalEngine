import time
import random
from threading import Lock

class RateLimiter:
    def __init__(self, min_interval=1.00, max_interval=2.00):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.last_request_time = 0
        self.lock = Lock()
    
    def wait(self):
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.last_request_time
            interval = random.uniform(self.min_interval, self.max_interval)
            
            if elapsed < interval:
                wait_time = interval - elapsed
                time.sleep(wait_time)
            
            self.last_request_time = time.time()