from multiprocessing.pool import Pool
import os
import json
import contextlib


# DOES NOT WORK ON LINUX


def run():
    for _ in range(100):
        print("run")
        try:
            fd = os.open("test.json", os.O_RDWR | os.O_EXLOCK)
            counter = json.loads(os.read(fd, 1000))
            counter["counter"] += 1

            os.lseek(fd, 0, 0)
            os.truncate(fd, 0)
            os.write(fd, json.dumps(counter).encode())
        except BaseException as e:
            print(e)
        finally:
            os.close(fd)


if __name__ == "__main__":
    with contextlib.suppress(FileExistsError):
        fd = os.open("test.json", os.O_CREAT | os.O_RDWR | os.O_EXCL)
        os.write(fd, json.dumps({"counter": 0}).encode())
        os.close(fd)
    pool = Pool(10)
    for _ in range(10):
        pool.apply_async(run)
    pool.close()
    pool.join()
