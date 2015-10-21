#!/usr/bin/python
import unittest
import arrow
import gs

class dateTimeTestCase(unittest.TestCase):
    def test_future_time(self):
        now = arrow.now("Europe/London")
        assert gs.parse_time("1h40m", now) == now.replace(hours = 1, minutes = 40)
        assert gs.parse_time("50m", now) == now.replace(minutes = 50)
        assert gs.parse_time("10h", now) == now.replace(hours = 10)
        assert gs.parse_time("100m", now) == now.replace(minutes = 100)
        assert gs.parse_time("100h", now) == now.replace(hours = 100)

class windowTestCase(unittest.TestCase):
    def test_window(self):
        now = arrow.now("Europe/London")
        pass

if __name__ == '__main__':
    import nose
    nose.main()
