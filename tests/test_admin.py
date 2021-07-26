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
            "username": "user3",
            "password": "password",
            "email": "user3@a.a",
            "is_admin": False,
        }
        self.data_bad_too_short_password = {
            "username": "user3",
            "password": "short",
            "email": "user3@a.a",
            "is_admin": False,
        }
        self.data_bad_empty_field = {"username": "user3"}
        self.data_bad_username_duplicate = {
            "username": "user",
            "password": "useruser",
            "email": "user@a.a",
        }
        self.data_bad_email_duplicate = {
            "username": "user3",
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
        self.assertIn(b"This field is required.", res.data)

    def test_post_bad_username_duplicate(self):
        res = self.post(login="admin", data=self.data_bad_username_duplicate)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The username or the email has been used.", res.data)

    def test_post_bad_email_duplicate(self):
        res = self.post(login="admin", data=self.data_bad_email_duplicate)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The username or the email has been used.", res.data)


class ManageUserBackend(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("admin.manage_user_backend")
        self.patch_data_ok = {"user_id": 1, "email": "user2@a.a"}
        self.patch_data_bad_duplicate_email = {"user_id": 2, "email": "user@user.com"}
        self.patch_data_bad_duplicate_username = {"user_id": 2, "username": "user"}
        self.patch_data_bad_too_short_password = {"user_id": 1, "password": "short"}
        self.patch_data_bad_user_not_exists = {"user_id": 10, "username": "user10"}
        self.delete_data_ok = {"user_id": 2}
        self.delete_data_bad_user_not_exists = {"user_id": 10}

    def patch(self, data=None):
        self.login("admin")
        res = self.client.patch(self.route, json=data, follow_redirects=True)
        return res

    def delete(self, data=None):
        self.login("admin")
        res = self.client.delete(self.route, json=data, follow_redirects=True)
        return res

    def test_patch_ok(self):
        res = self.patch(self.patch_data_ok)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"T;OK.", res.data)

    def test_patch_bad_duplicate_email(self):
        res = self.patch(self.patch_data_bad_duplicate_email)
        self.assertEqual(res.status_code, 400)
        self.assertIn(b"F;The email has been used.", res.data)

    def test_patch_bad_duplicate_username(self):
        res = self.patch(self.patch_data_bad_duplicate_username)
        self.assertEqual(res.status_code, 400)
        self.assertIn(b"F;The username has been used.", res.data)

    def test_patch_bad_too_short_password(self):
        res = self.patch(self.patch_data_bad_too_short_password)
        self.assertEqual(res.status_code, 400)
        self.assertIn(b"F;The password must contain at least 6 characters.", res.data)

    def test_patch_bad_user_not_exists(self):
        res = self.patch(self.patch_data_bad_user_not_exists)
        self.assertEqual(res.status_code, 400)
        self.assertIn(b"F;The user does not exist.", res.data)

    def test_delete_ok(self):
        res = self.delete(self.delete_data_ok)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"T;OK.", res.data)

    def test_delete_bad_user_not_exists(self):
        res = self.delete(self.delete_data_bad_user_not_exists)
        self.assertEqual(res.status_code, 400)
        self.assertIn(b"F;The user does not exist.", res.data)
