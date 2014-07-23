===============
Redis-Semaphore
===============

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
    semaphore = Semaphore(Redis(), count=2, namespace='example')
    # initialize session with something access
    with semaphore: # remaining 1 resource
        # do something
        with semaphore: # remaining 0 resource
            # do something
            pass
        with semaphore: # remaining 0 resource
            # do something
            pass

