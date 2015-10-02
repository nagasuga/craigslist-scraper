import json
from unittest import TestCase

from ..client import Craigslist


class CraigslistTest(TestCase):
    def setUp(self):
        self.craigslist = Craigslist()

    def read_file(self, file_path):
        with open(file_path, 'r') as f_obj:
            return f_obj.read()

    def test_call(self):
        for entry in self.craigslist.call(query='macbook pro').iter():
            print(entry)
