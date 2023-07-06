import httpretty
import unittest

# Enable httpretty for all tests in the current module
def enable_httpretty():
    httpretty.enable()

# Disable httpretty and reset the state after each test
def disable_httpretty():
    httpretty.disable()
    httpretty.reset()

# Set up a test class with httpretty enabled
class HttprettyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        httpretty.enable()

    def tearDown(self):
        httpretty.reset()

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()