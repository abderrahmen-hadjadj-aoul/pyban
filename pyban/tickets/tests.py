from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse
import json

class UserTests(TestCase):

    # HELPERS

    def create_user(self, username, email, password):
        client = Client()
        payload = {
            "username": username,
            "email": email,
            "password": password,
        }
        response = client.post(reverse("tickets:users"), payload)
        user = json.loads(response.content)
        return (response, user)

    def get_user(self, id):
        client = Client()
        response = client.get(reverse("tickets:user", kwargs={"user_id": id}))
        user = json.loads(response.content)
        return (response, user)

    def get_users(self):
        client = Client()
        response = client.get(reverse("tickets:users"))
        data = json.loads(response.content)
        return (response, data)

    # TESTS

    def test_create_user(self):
        """
        A user should be created
        """
        username = "Tom"
        email = "test@gmail.com"
        password = "123"
        (response, user) = self.create_user(username, email, password)
        self.assertIs(response.status_code, 201)
        self.assertEqual(user['username'], username)
        self.assertEqual(user['email'], email)

    def test_create_user_witout_username(self):
        """
        A user created without username should return an error
        """
        username = ""
        email = "test@gmail.com"
        password = "123"
        (response, data) = self.create_user(username, email, password)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Username must be set")

    def test_create_user_twice(self):
        """
        A user created twice should return an error
        """
        username = "Tom"
        email = "test@gmail.com"
        password = "123"
        (response, user) = self.create_user(username, email, password)
        self.assertIs(response.status_code, 201)
        self.assertEqual(user['username'], username)
        self.assertEqual(user['email'], email)
        (response, data) = self.create_user(username, email, password)
        self.assertEqual(data['message'], "User already exists")

    def test_create_then_get_user(self):
        """
        A user should be created then get
        """
        username = "Tom2"
        email = "test2@gmail.com"
        password = "1232"
        (response, created_user) = self.create_user(username, email, password)
        id = created_user['id']
        (response, user) = self.get_user(id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user['username'], username)
        self.assertEqual(user['email'], email)

    def test_get_user_not_exist(self):
        """
        An error should be returned
        """
        id = 123456789
        (response, user) = self.get_user(id)
        self.assertEqual(response.status_code, 404)

    def test_get_users(self):
        """
        Should get users
        """
        username = "Tom3"
        email = "test3@gmail.com"
        password = "1233"
        (response, created_user) = self.create_user(username, email, password)
        (response, data) = self.get_users()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['users']), 1)
        self.assertEqual(data['users'][0]['username'], username)
        self.assertEqual(data['users'][0]['email'], email)
