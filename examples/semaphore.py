#-*- coding:utf-8 -*-
from redis import Redis
from redis_semaphore import Semaphore
from threading import Thread
import urllib2
import time

semaphore = Semaphore(Redis(), count=2, namespace='example')


def task():
    url = 'https://www.google.co.jp/'
    with semaphore:
        print(urllib2.urlopen(url).code)
        time.sleep(2)


def main():
    threads = list()
    for _ in range(5):
        threads.append(Thread(target=task))
    for th in threads:
        th.start()
    for th in threads:
        th.join()

if __name__ == '__main__':
    main()
