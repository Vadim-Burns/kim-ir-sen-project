"""
This file contains api tests

Instruction:
1. Start server.py on port 8080
2. Start this fil
3. Check out results
"""
import unittest

import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:8080"

    """
    Testing correct working
    """

    def test_create_note(self):
        text = "Encrypting some weird text"

        answer = requests.post(self.URL + "/api/add", json={"text": text})

        self.assertTrue(
            200 <= answer.status_code < 300,
            "Incorrect answer status code after sending correct request for creating note"
        )

        self.assertTrue(
            answer.json()["key"] is not None,
            "No key after sending correct request for creating note"
        )

    def test_get_note(self):
        text = "Encrypting some weird text"

        # Create note
        key = requests.post(self.URL + "/api/add", json={"text": text}).json().get("key")

        # Get note
        answer = requests.post(self.URL + "/api/get", json={"key": key})

        self.assertTrue(
            200 <= answer.status_code < 300,
            "Incorrect answer status code after sending correct request for getting note"
        )

        self.assertTrue(
            answer.json()["text"] is not None,
            "No text after sending correct request for getting note"
        )

    def test_create_get_text_identical(self):
        text = "Encrypting some weird text"

        key = requests.post(self.URL + "/api/add", json={"text": text}).json().get("key")
        new_text = requests.post(self.URL + "/api/get", json={"key": key}).json().get("text")

        self.assertEqual(new_text, text, "Start and final texts are not identical")

    """
    Testing error answers
    """

    def test_create_no_json_error(self):
        answer = requests.post(self.URL + "/api/add")

        self.assertEqual(
            answer.status_code,
            400,
            "Wrong status code after sending post request to /api/add with empty body"
        )

        self.assertEqual(
            answer.json()["error"],
            "json data is not valid",
            "Wrong error after sending post request to /api/add with empty body"
        )

    def test_create_wrong_json_error(self):
        answer = requests.post(self.URL + "/api/add", json={"nothing": "nothing"})

        self.assertEqual(
            answer.status_code,
            400,
            "Wrong status code after sending post request to /api/add with wrong json"
        )

        self.assertEqual(
            answer.json()["error"],
            "json data is not valid",
            "Wrong error after sending post request to /api/add with wrong json"
        )

    def test_get_no_json_error(self):
        answer = requests.post(self.URL + "/api/get")

        self.assertEqual(
            answer.status_code,
            400,
            "Wrong status code after sending post request to /api/get with empty body"
        )

        self.assertEqual(
            answer.json()["error"],
            "json data is not valid",
            "Wrong error after sending post request to /api/get with empty body"
        )

    def test_get_wrong_json_error(self):
        answer = requests.post(self.URL + "/api/get", json={"nothing": "nothing"})

        self.assertEqual(
            answer.status_code,
            400,
            "Wrong status code after sending post request to /api/add with wrong json"
        )

        self.assertEqual(
            answer.json()["error"],
            "json data is not valid",
            "Wrong error after sending post request to /api/add with wrong json"
        )

    def test_get_wrong_key_error(self):
        answer = requests.post(
            self.URL + "/api/get",
            json={
                "key": "gAAAAABhRf19CDB9l8gw467nCR8DJ0Dr_qAWABNrsRdcbC_dMzFKISA_VKaowQq-T7fLAka4JJp5JujmBTiPACRH7KfLuOcrBBhMOecBhT1R-tOpGdUpsT2tKhRVem6587GIHdBDkasI"
            }
        )

        self.assertEqual(
            answer.status_code,
            403,
            "Wrong status code after sending post request to /api/add with wrong key"
        )

        self.assertEqual(
            answer.json()["error"],
            "Invalid key",
            "Wrong error after sending post request to /api/add with wrong key"
        )

    def test_note_not_found_error(self):
        text = "Encrypting some weird text"

        # Create note
        key = requests.post(self.URL + "/api/add", json={"text": text}).json().get("key")

        # Delete note from database
        requests.post(self.URL + "/api/get", json={"key": key})

        # Request that note again
        answer = requests.post(self.URL + "/api/get", json={"key": key})

        self.assertEqual(
            answer.status_code,
            403,
            "Wrong status code after sending deleted note's key to /api/get"
        )

        self.assertEqual(
            answer.json()["error"],
            "Invalid key",
            "Wrong error after sending deleted note's key to /api/get"
        )
