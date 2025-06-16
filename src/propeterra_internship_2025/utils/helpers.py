import time


def timing_function(func):
    '''
    A decorator function that measures the amount of time
    needed for a function to run
    '''

    def measure_time(*args, **kwargs):

        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time,
        print(f"function took {total_time} seconds to run")
        return total_time


    return measure_time