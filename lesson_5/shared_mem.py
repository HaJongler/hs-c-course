import random
import time
from multiprocessing import Process, Lock, Value

def f(l, v, id):
    while True:
        l.acquire()
        print '{}: I see the value {} in the shared memory!'.format(id, v.value)

        new_val = random.randint(0, 100000)
        print '{}: I am placing new value: {}'.format(id, new_val)
        v.value = new_val

        l.release()
        time.sleep(random.randint(0,3))

if __name__ == '__main__':
    lock = Lock()
    num = Value('d', 0.0)

    pa = Process(target=f, args=(lock, num, 'p1')).start()
    pb = Process(target=f, args=(lock, num, 'p2')).start()