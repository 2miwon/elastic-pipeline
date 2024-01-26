def bench_mark(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Function {func.__name__} took {time.time() - start} seconds to run')
        return result