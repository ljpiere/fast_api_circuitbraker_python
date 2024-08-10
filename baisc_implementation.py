import time
import random

class CircuitBreaker:
    def __init__(self, max_failures, reset_timeout):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF-OPEN"
            else:
                raise Exception("CircuitBreaker is OPEN. No calls allowed.")

        try:
            result = func(*args, **kwargs)
            self.reset()
            return result
        except Exception as e:
            self.record_failure()
            if self.failure_count >= self.max_failures:
                self.trip()
            raise e

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

    def reset(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def trip(self):
        self.state = "OPEN"

def risky_operation():
    if random.random() < 0.7:
        raise Exception("Operation failed!")
    return "Operation succeeded!"

# Test del Circuit Breaker
breaker = CircuitBreaker(max_failures=3, reset_timeout=5)

for i in range(10):
    try:
        result = breaker.call(risky_operation)
        print(result)
    except Exception as e:
        print(f"Attempt {i + 1}: {e}")
    time.sleep(1)
