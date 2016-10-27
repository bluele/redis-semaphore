# -*- coding:utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from redis import StrictRedis
from redis_semaphore import Semaphore


class SimpleTestCase(TestCase):

    def setUp(self):
        self.client = StrictRedis()
        self.s_count = 2
        self.sem1 = Semaphore(
            client=self.client,
            count=self.s_count
        )
        self.sem1.reset()
        self.sem2 = Semaphore(
            client=self.client,
            count=self.s_count
        )
        self.sem2.reset()
        self.sem3 = Semaphore(
            client=self.client,
            count=self.s_count,
            blocking=False
        )
        self.sem3.reset()

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

    def test_create_with_existing(self):
        with self.sem1 as sem1:
            with self.sem2 as sem2:
                assert sem1.available_count == 0
                assert sem2.available_count == 0
                sem3 = Semaphore(client=self.client, count=40)
                assert sem3.available_count == 0

    def test_nonblocking(self):
        from redis_semaphore import NotAvailable
        for _ in range(self.s_count):
            self.sem3.acquire()
        assert self.sem3.available_count == 0

        with self.assertRaises(NotAvailable):
            with self.sem3:
                assert False, 'should never reach here'


if __name__ == '__main__':
    from os.path import dirname, abspath
    import sys
    import unittest
    d = dirname
    current_path = d(d(abspath(__file__)))
    sys.path.append(current_path)
    unittest.main()
