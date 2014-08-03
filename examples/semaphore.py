#-*- coding:utf-8 -*-
from redis import Redis
from redis_semaphore import Semaphore
from threading import Thread
import urllib2
import time

semaphore = Semaphore(Redis(), count=2, namespace='example')


def task(i):
    url = 'https://www.google.co.jp/'
    with semaphore:
        print('id: {} => {}'.format(i, urllib2.urlopen(url).code))
        print('sleep...')
        time.sleep(2)


def main():
    threads = list()
    for i in range(5):
        threads.append(Thread(target=task, args=(i,)))
    for th in threads:
        th.start()
    for th in threads:
        th.join()

if __name__ == '__main__':
    main()
