from multiprocessing.pool import Pool
import os
import json
import contextlib
import fcntl
import time


RUNS_PER_WORKER = 30_000
WORKERS = 10


def writer():
    for _ in range(RUNS_PER_WORKER):
        with open("test.json", "r+b") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            counter = json.loads(f.read())
            counter["counter"] += 1
            f.seek(0)
            f.write(json.dumps(counter).encode())
            f.truncate()


def reader():
    for _ in range(RUNS_PER_WORKER):
        with open("test.json", "r+") as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            counter = json.loads(f.read())


if __name__ == "__main__":
    t1 = time.time()
    with contextlib.suppress(FileExistsError):
        fd = os.open("test.json", os.O_CREAT | os.O_RDWR | os.O_EXCL)
        os.write(fd, json.dumps({"counter": 0}).encode())
        os.close(fd)
    pool = Pool(WORKERS)
    for _ in range(WORKERS):
        pool.apply_async(writer)
        pool.apply_async(reader)
    pool.close()
    pool.join()
    td = time.time() - t1
    print(f"Time: {td:.2f} seconds, per second: {WORKERS * RUNS_PER_WORKER / td:.2f}")
