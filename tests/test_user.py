from flask import url_for
from tests.helper import TestModel


class LoginPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("user.login_page")
        self.user_data_bad_wrong_password = {"username": "user", "password": "bad"}
        self.user_data_bad_empty_field = {"username": "user"}

    def test_get_with_no_auth(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_get_with_auth(self):
        res = self.get(login="user")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Dashboard", res.data)

    def test_post_ok(self):
        res = self.post(data=self.user_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Dashboard", res.data)

    def test_post_bad_wrong_password(self):
        res = self.post(data=self.user_data_bad_wrong_password)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Wrong username or password.", res.data)

    def test_post_bad_empty_field(self):
        res = self.post(data=self.user_data_bad_empty_field)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"This field is required.", res.data)


class RegisterPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("user.register_page")
        self.register_data_ok = {
            "username": "user2",
            "password": "useruser",
            "repeat_password": "useruser",
            "email": "user@a.a",
        }
        self.register_data_bad_username_duplicate = {
            "username": "user",
            "password": "useruser",
            "repeat_password": "useruser",
            "email": "user@a.a",
        }
        self.register_data_bad_email_duplicate = {
            "username": "user2",
            "password": "useruser",
            "repeat_password": "useruser",
            "email": "user@user.com",
        }
        self.register_data_bad_too_short_password = {
            "username": "user2",
            "password": "short",
            "repeat_password": "short",
            "email": "user@a.a",
        }
        self.register_data_bad_empty_field = {
            "username": "user2",
        }

    def test_get_with_no_auth(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_get_with_auth(self):
        res = self.get(login="user")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Dashboard", res.data)

    def test_post_ok(self):
        res = self.post(data=self.register_data_ok)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_post_bad_username_duplicate(self):
        res = self.post(data=self.register_data_bad_username_duplicate)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The username or the email has been used.", res.data)

    def test_post_bad_email_duplicate(self):
        res = self.post(data=self.register_data_bad_email_duplicate)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The username or the email has been used.", res.data)

    def test_post_bad_too_short_password(self):
        res = self.post(data=self.register_data_bad_too_short_password)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The password must contain at least 6 characters.", res.data)

    def test_post_bad_empty_field(self):
        res = self.post(data=self.register_data_bad_empty_field)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"This field is required.", res.data)


class DashboardPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("user.dashboard_page")

    def test_get_with_no_auth(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_get_with_auth(self):
        res = self.get(login="user")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Dashboard", res.data)


class SettingPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("user.setting_page")
        self.data_ok = {"email": "user@a.a"}
        self.data_bad_too_short_password = {"email": "user@a.a", "password": "short"}
        self.data_bad_empty_field = {}
        self.data_bad_duplicate_email = {"email": "user@user.com"}

    def test_get_with_no_auth(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_get_with_auth(self):
        res = self.get(login="user")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Setting", res.data)

    def test_post_ok(self):
        res = self.post(login="user", data=self.data_ok)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"OK.", res.data)

    def test_post_bad_too_short_password(self):
        res = self.post(login="user", data=self.data_bad_too_short_password)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The password must contain at least 6 characters.", res.data)

    def test_post_bad_empty_field(self):
        res = self.post(login="user", data=self.data_bad_empty_field)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"This field is required.", res.data)

    def test_post_bad_duplicate_email(self):
        res = self.post(login="user", data=self.data_bad_duplicate_email)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The email has been used.", res.data)
