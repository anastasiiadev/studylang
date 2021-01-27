'''import threading
import time


def my_timer(print_interval):
    data = threading.local()
    data.counter = 1
    while True:
        time.sleep(print_interval)
        print("I am alive %d times!" % data.counter, threading.current_thread().name)
        data.counter += 1

if __name__=="__main__":
    t = threading.Thread(target=my_timer, name="My time thread", args=(5,), daemon=True)
    t.start()

import time
import threading as th


def target(form):
    while True:
        print(form)  # нажмите кнопку тут
        form += 1
        #time.sleep(10)


form = 1  # некая кнопка
t = th.Thread(target=target, args=(form,), daemon=True)
t.start()
# сохраните куда-то переменную t
# del t если вам надо убить поток'''

import datetime, threading

def foo():
    print(datetime.datetime.now())
    threading.Timer(1, foo).start()

foo()
