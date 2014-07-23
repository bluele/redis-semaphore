#-*- coding:utf-8 -*-
from unittest import TestCase


class SimpleTestCase(TestCase):

    def setUp(self):
        from redis import Redis
        from redis_semaphore import Semaphore
        self.client = Redis()
        self.s_count = 2
        self.sem1 = Semaphore(
            client=self.client,
            count=self.s_count
        )
        self.sem2 = Semaphore(
            client=self.client,
            count=self.s_count
        )

    def test_lock(self):
        assert self.sem1.available_count == self.s_count
        assert self.sem1.acquire() is not None
        assert self.sem1.available_count == (self.s_count - 1)
        self.sem1.release()
        assert self.sem1.available_count == self.s_count

        assert self.sem2.available_count == self.s_count
        assert self.sem1.acquire() is not None
        assert self.sem2.available_count == (self.s_count - 1)
        self.sem1.release()

    def test_with(self):
        assert self.sem1.available_count == self.s_count
        with self.sem1 as sem:
            assert sem.available_count == (self.s_count - 1)
            with sem:
                assert sem.available_count == (self.s_count - 2)
        assert self.sem1.available_count == self.s_count

if __name__ == '__main__':
    from os.path import dirname, abspath
    import sys
    import unittest
    d = dirname
    current_path = d(d(abspath(__file__)))
    sys.path.append(current_path)
    unittest.main()
