import unittest
from time import sleep
from flask import url_for
from app import create_app
from tests.helper import TestModel, generate_test_data
from app.KV import kv


class IndexPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("main.index_page")
        self.url_ok = {"old": "https://example.com", "new": "ex"}
        self.url_bad_characters = {"old": "https://example.com", "new": "%%%$123"}
        self.url_bad_empty = {"old": "https://example.com"}

    def test_get_with_no_auth(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)
        self.assertIn(b"Register", res.data)

    def test_get_with_auth(self):
        res = self.get(login="user")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Dashboard", res.data)

    def test_post_ok(self):
        res = self.post(data=self.url_ok)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Successfully add this record.", res.data)

    def test_post_bad_characters(self):
        res = self.post(data=self.url_bad_characters)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Bad characters in the field.", res.data)

    def test_post_bad_empty(self):
        res = self.post(data=self.url_bad_empty)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"This field is required.", res.data)


class RedirectPageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("test")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        generate_test_data()
        kv.write("https://google.com", "test1")
        kv.write("https://github.com", "gh")
        self.route_ok = "/test1"
        self.route_not_found = "/wrong"

    def tearDown(self) -> None:
        kv.delete("test1")
        kv.delete("gh")
        if self.app_context is not None:
            self.app_context.pop()

    def test_ok(self):
        res = self.client.get(self.route_ok)
        self.assertEqual(res.status_code, 302)

    def test_not_found(self):
        res = self.client.get(self.route_not_found)
        self.assertEqual(res.status_code, 404)
