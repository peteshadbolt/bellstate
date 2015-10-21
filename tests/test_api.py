#!/usr/bin/python
from gs import app, redis
import unittest
import json
import flask
import time
import arrow

TEST_BASE = {"REMOTE_ADDR": "test"}
JSON_HEADER = [("Accept", "application/json")]


class APITestCase(unittest.TestCase):

    def setUp(self):
        """ Pre testing """
        self.app = app.test_client()

    def tearDown(self):
        """ Post testing """
        redis.flushdb()

    def test_something(self):
        """ First attempt at an API"""
        response = self.app.put('/rave/now', environ_base=TEST_BASE, headers=JSON_HEADER)
        assert response.status_code == 200


if __name__ == '__main__':
    import nose
    nose.main()
