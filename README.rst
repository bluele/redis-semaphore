===============
Redis-Semaphore
===============

.. image:: https://travis-ci.org/bluele/redis-semaphore.svg?branch=master
    :target: https://travis-ci.org/bluele/redis-semaphore


A distributed semaphore and mutex built on Redis.


Installation
------------
To install redis-semaphore, simply::

    pip install redis-semaphore


Or alternatively, you can download the repository and install manually by doing::

    git clone git@github.com:bluele/redis-semaphore.git
    cd redis-semaphore
    python setup.py install


Examples
--------

::

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
