import os
from time import sleep
from loky import get_reusable_executor


def say_hello(k, y):
    pid = os.getpid()
    print(f"Hello from {pid} with arg {k} and {y}")
    sleep(.01)
    return pid


# Create an executor with 4 worker processes, that will
# automatically shutdown after idling for 2s
executor = get_reusable_executor(max_workers=4, timeout=2)

res = executor.submit(say_hello, 1, 2)
print("Got results:", res.result())

# results = executor.map(say_hello, range(50))

# print("yolo", results)