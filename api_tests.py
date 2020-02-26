import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:8080"

    def test_api_correct(self):
        text = "Encrypting some weird text"

        key = requests.post(self.URL + "/api/add", json={"text": text}).json().get("key")

        new_text = requests.post(self.URL + "/api/get", json={"key": key}).json().get("text")
        self.assertEqual(new_text, text, "Начальный и разшифрованный тексты не совпадают")

    def test_api_incorrect(self):
        code = requests.post(self.URL + "/api/add").status_code
        self.assertEqual(code, 400)

        code = requests.post(self.URL + "/api/add", json={"nothing": "nothing"}).status_code
        self.assertEqual(code, 400)

        code = requests.post(self.URL + "/api/get").status_code
        self.assertEqual(code, 400)

        code = requests.post(self.URL + "/api/get", json={"nothing": "nothing"}).status_code
        self.assertEqual(code, 400)

        r = requests.post(self.URL + "/api/get", json={"key": "wrong"})
        code = r.status_code
        error = r.json().get("error")
        self.assertEqual(error, "Wrong key")
        self.assertEqual(code, 404)