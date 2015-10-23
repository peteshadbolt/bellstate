#!/usr/bin/python
from bellstate import app
from bellstate import redis
import unittest
import json
import flask
from random import random

TEST_BASE = {"REMOTE_ADDR": "test"}
JSON_HEADER = [("Accept", "application/json")]

class APITestCase(unittest.TestCase):

    def setUp(self):
        """ Pre testing """
        self.app = app.test_client()

    def tearDown(self):
        """ Post testing """
        redis.flushdb()

    def simple_test(self):
        """ First attempt at an API"""
        response = self.app.get('/alice/heads')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["bob"]=={}

    def cheat_test(self):
        """ Check that we get all the data needed to cheat """
        response = self.app.get('/alice/heads')
        response = self.app.get('/bob/heads')
        data = json.loads(response.data)
        assert data["alice"]!={}
        assert data["bob"]!={}
        assert "coin" in data["alice"] and "color" in data["alice"]

    def runonce(self):
        a = "heads" if random()<0.5 else "tails"
        b = "heads" if random()<0.5 else "tails"
        r = self.app.get('/alice/'+a)
        r = self.app.get('/bob/'+b)
        data = json.loads(r.data)
        A = data["alice"]["color"]
        B = data["bob"]["color"]

        if a=="tails" and b=="tails":
            return A!=B
        else:
            return A==B

    def bell_test(self):
        """ Runs an actual Bell test and checks for violation """
        score = 0
        for i in range(100):
            score += self.runonce()
        assert score>75
        assert score<100
            



if __name__ == '__main__':
    import nose
    nose.main()
