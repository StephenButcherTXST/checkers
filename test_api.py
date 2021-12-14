import unittest
from json import dumps
from api import main

valid_grid = [
    ["R","R","B","-","B","B","B","-"],
    ["B","R","B","B","B","B","-","-"],
    ["B","R","B","B","R","R","-","B"],
    ["R","R","R","-","-","R","R","R"],
    ["B","B","B","R","-","-","-","B"],
    ["-","R","B","B","B","B","-","B"],
    ["R","B","-","B","R","B","-","R"],
    ["B","R","-","R","B","-","-","-"]
]

invalid_grid = [
    ["R","R","B","-","B","B","B","-"],
    ["B","R","B","B","B","B","-","-"],
    ["B","R","B","B","R","R","-","B"],
    ["R","R","R","-","-","R","R","R"],
    ["B","B","B","R","-","-","-","B"],
    ["-","R","B","B","B","B","B"],
    ["R","B","-","B","R","B","-","R"],
    ["B","R","-","R","B","-","-","-"]
]

class ApiTest(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_valid_grid(self):
        response = self.app.post('/', json=valid_grid)
        self.assertEqual(200, response.status_code)

    def test_invalid_grid(self):
        response = self.app.post('/', json=invalid_grid)
        self.assertEqual(400, response.status_code)
