import time


def load():
    for i in range(100):
        print(".", end="")
        time.sleep(0.5)

load()
