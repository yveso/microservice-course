import json
import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    def test_users(self):
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "yves", "email": "yves@yves.com"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("yves@yves.com was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Error is thrown if json is empty"""
        with self.client:
            response = self.client.post(
                "/users", data=json.dumps({}), content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_json_invalid_json_keys(self):
        """Error is thrown if json has no key username"""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "yves@yves.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Error is thrown if email already exists"""
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "yves", "email": "yves@yves.com"}
                ),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "yves", "email": "yves@yves.com"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Email already exists", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user(username="yves", email="yves@yves.com")
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("yves", data["data"]["username"])
            self.assertIn("yves@yves.com", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Error if id is no number"""
        # Lass das lieber das Framework machen 😁
        # @users_blueprint.route("/users/<int:user_id>")
        with self.client:
            response = self.client.get("/users/foobar")
            # data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            # self.assertIn("User doesn't exist", data["message"])
            # self.assertIn("fail", data["status"])

    def test_single_user_unknown_id(self):
        """Error if id is unknown"""
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User doesn't exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        add_user(username="yves", email="yves@yves.com")
        add_user(username="yves2", email="yves2@yves.com")
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("yves", data["data"]["users"][0]["username"])
            self.assertIn("yves@yves.com", data["data"]["users"][0]["email"])
            self.assertIn("yves2", data["data"]["users"][1]["username"])
            self.assertIn("yves2@yves.com", data["data"]["users"][1]["email"])
            self.assertIn("success", data["status"])

    def test_index_no_users(self):
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertIn(b"No users", response.data)

    def test_index_with_users(self):
        add_user(username="max", email="max@m.com")
        add_user(username="moritz", email="moritz@m.com")
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"No users", response.data)
            self.assertIn(b"max", response.data)
            self.assertIn(b"moritz", response.data)

    def test_index_add_users(self):
        with self.client:
            response = self.client.post(
                "/",
                data=dict(username="susi", email="susi@susi.com"),
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"No users", response.data)
            self.assertIn(b"susi", response.data)


if __name__ == "__main__":
    unittest.main()
