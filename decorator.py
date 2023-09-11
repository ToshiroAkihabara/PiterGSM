import time


def time_of_working(func):
    def wrapper(*args, **kwargs):
        time_start = time.time()
        func(*args, **kwargs)
        time_end = time.time() - time_start
        print("Затраченное время: {} секунд".format(time_end))

    return wrapper
