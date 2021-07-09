from flask import url_for
from tests.helper import TestModel


class DashboardPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("admin.dashboard_page")

    def test_get_with_no_auth(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_get_with_user_auth(self):
        res = self.get(login="user")
        self.assertEqual(res.status_code, 403)

    def test_get_with_admin_auth(self):
        res = self.get(login="admin")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Admin Dashboard", res.data)


class ManageUserPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("admin.manage_user_page")
        self.data_ok = {
            "username": "user2",
            "password": "password",
            "email": "user2@a.a",
            "is_admin": False,
        }
        self.data_bad_too_short_password = {
            "username": "user2",
            "password": "short",
            "email": "user2@a.a",
            "is_admin": False,
        }
        self.data_bad_empty_field = {"username": "user2"}
        self.data_bad_username_duplicate = {
            "username": "user",
            "password": "useruser",
            "email": "user@a.a",
        }
        self.data_bad_email_duplicate = {
            "username": "user2",
            "password": "useruser",
            "email": "user@user.com",
        }

    def test_get_with_no_auth(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_get_with_user_auth(self):
        res = self.get(login="user")
        self.assertEqual(res.status_code, 403)

    def test_get_with_admin_auth(self):
        res = self.get(login="admin")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Admin Dashboard", res.data)

    def test_post_ok(self):
        res = self.post(login="admin", data=self.data_ok)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Add user successfully.", res.data)

    def test_post_bad_too_short_password(self):
        res = self.post(login="admin", data=self.data_bad_too_short_password)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The password must contain at least 6 characters.", res.data)

    def test_post_bad_empty_field(self):
        res = self.post(login="admin", data=self.data_bad_empty_field)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The field is required.", res.data)

    def test_post_bad_username_duplicate(self):
        res = self.post(login="admin", data=self.data_bad_username_duplicate)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The username has been used.", res.data)

    def test_post_bad_email_duplicate(self):
        res = self.post(login="admin", data=self.data_bad_email_duplicate)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The email has been used.", res.data)


class ManageUserBackend(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("admin.manage_user_backend")

