from django.db import transaction
from django.test import TestCase, Client
from django.urls import reverse
from .models import User
import json


class GeneralTests(TestCase):
    def setUp(self):
        self.client = Client()

    # HELPERS

    def create_user(self, username, password):
        payload = {
            "username": username,
            "password": password,
        }
        response = self.client.post(reverse("tickets:users"),
                                    json.dumps(payload),
                                    content_type="application/json")
        user = json.loads(response.content)
        return (response, user)

    def get_user(self, id):
        response = self.client.get(
            reverse("tickets:user", kwargs={"user_id": id}))
        user = json.loads(response.content)
        return (response, user)

    def get_users(self):
        response = self.client.get(reverse("tickets:users"))
        data = json.loads(response.content)
        return (response, data)

    def get_token(self, username, password):
        payload = {
            "username": username,
            "password": password,
        }
        response = self.client.post(reverse("tickets:api_token_auth"),
                                    json.dumps(payload),
                                    follow=True,
                                    content_type="application/json")
        data = json.loads(response.content)
        return (response, data)

    # USERS
    def test_create_user(self):
        """
        A user should be created
        """
        username = "Tom"
        password = "123"
        (response, user) = self.create_user(username, password)
        self.assertIs(response.status_code, 201)
        self.assertEqual(user['username'], username)

    def test_create_user_witout_username(self):
        """
        A user created without username should return an error
        """
        username = ""
        password = "123"
        (response, data) = self.create_user(username, password)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Username must be set")

    def test_create_user_twice(self):
        """
        A user created twice should return an error
        """
        username = "Tom"
        password = "123"
        (response, user) = self.create_user(username, password)
        self.assertIs(response.status_code, 201)
        self.assertEqual(user['username'], username)
        (response, data) = self.create_user(username, password)
        self.assertEqual(data['message'], "User already exists")

    def test_create_then_get_user(self):
        """
        A user should be created then get
        """
        username = "Tom2"
        password = "1232"
        (response, created_user) = self.create_user(username, password)
        id = created_user['id']
        (response, user) = self.get_user(id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user['username'], username)

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
        password = "1233"
        (response, created_user) = self.create_user(username, password)
        (response, data) = self.get_users()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['users']), 1)
        self.assertEqual(data['users'][0]['username'], username)

    def test_get_token(self):
        """
        Should log properly with right credentials
        """
        username = "Tom3"
        password = "1233"
        (response, created_user) = self.create_user(username, password)
        (response, data) = self.get_token(username, password)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", data)

    def test_login_wrong_username(self):
        """
        Should return an error for wrong credentials
        """
        username = "Tom3"
        password = "1233"
        (response, created_user) = self.create_user(username, password)
        (response, data) = self.get_token(username + "0", password)
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_password(self):
        """
        Should return an error for wrong credentials
        """
        username = "Tom3"
        password = "1233"
        (response, created_user) = self.create_user(username, password)
        (response, data) = self.get_token(username, password + "0")
        self.assertEqual(response.status_code, 400)

    # BOARD

    def create_board(self, name, headers={}):
        payload = {
            "name": name,
        }
        response = self.client.post(reverse("tickets:boards"),
                                    json.dumps(payload),
                                    content_type="application/json",
                                    **headers)
        board = json.loads(response.content)
        return (response, board)

    def get_board(self, board_id, headers={}):
        response = self.client.get(
            reverse("tickets:board", kwargs={"pk": board_id}), **headers)
        board = {}
        try:
            board = json.loads(response.content)
        except Exception:
            pass
        return (response, board)

    def test_board_create(self):
        """
        Should create a board
        """
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        id = created_user["id"]
        user = User.objects.get(pk=id)
        name = "Board Name"
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        (response, created_board) = self.create_board(name, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_board["name"], name)

    def test_board_create_then_get_it(self):
        """
        Should get the created board
        """
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        userid = created_user["id"]
        user = User.objects.get(pk=userid)
        # Get token
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        # Create board
        name = "Board Name"
        (response, created_board) = self.create_board(name, headers=headers)
        self.assertEqual(response.status_code, 201)
        boardid = created_board["id"]
        # Get board
        (response, board) = self.get_board(boardid, headers=headers)
        self.assertEqual(board["id"], boardid)
        self.assertEqual(board["name"], name)

    def test_board_get_not_exist(self):
        """
        Should return error for board that does not exist
        """
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        userid = created_user["id"]
        user = User.objects.get(pk=userid)
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        boardid = 12346789
        (response, board) = self.get_board(boardid, headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_board_permission(self):
        """
        Should return error for no permission of board
        """
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        username2 = "Tom--"
        password2 = "123--"
        (response, created_user2) = self.create_user(username2, password2)
        # Get token
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        (response2, data2) = self.get_token(username2, password2)
        token2 = data2["token"]
        headers2 = {"HTTP_AUTHORIZATION": "Token " + token2}
        # Create board
        name = "Board Name"
        (response, created_board) = self.create_board(name, headers=headers)
        self.assertEqual(response.status_code, 201)
        boardid = created_board["id"]
        # Get board
        (response, board) = self.get_board(boardid, headers=headers2)
        self.assertEqual(response.status_code, 401)

    def test_get_board_list(self):
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        # Get token
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        # Create boards
        created_boards = []
        number_of_boards = 5
        for n in range(number_of_boards):
            name = "Board Name" + str(n)
            (response, created_board) = self.create_board(name,
                                                          headers=headers)
            created_boards.append((response, created_board))
        response = self.client.get(reverse("tickets:boards"), **headers)
        boards = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(boards), 5)
        for n in range(number_of_boards):
            self.assertIn(created_boards[n][1], boards)

    def test_get_board_list_without_other_users_boards(self):
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        username2 = "Tom--"
        password2 = "123--"
        (response2, created_user2) = self.create_user(username2, password2)
        # Get token
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        (response2, data2) = self.get_token(username2, password2)
        token2 = data2["token"]
        headers2 = {"HTTP_AUTHORIZATION": "Token " + token2}
        # Create boards
        created_boards = []
        number_of_boards = 5
        for n in range(number_of_boards):
            name = "Board Name" + str(n)
            (response, created_board) = self.create_board(name,
                                                          headers=headers)
            created_boards.append((response, created_board))
            name = "Board Name Other" + str(n)
            (response, created_board) = self.create_board(name,
                                                          headers=headers2)
        response = self.client.get(reverse("tickets:boards"), **headers)
        boards = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(boards), 5)
        for n in range(number_of_boards):
            self.assertIn(created_boards[n][1], boards)

    # TICKETS

    def test_create_ticket(self):
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        # Create board
        name = "Board Name for tickets"
        (response, created_board) = self.create_board(name, headers=headers)
        self.assertEqual(response.status_code, 201)
        boardid = created_board["id"]
        # Create ticket
        payload = {
            "title": "Ticket Title",
            "description": "Ticket Description",
            "board": boardid,
        }
        response = self.client.post(reverse("tickets:tickets"),
                                    json.dumps(payload),
                                    content_type="application/json",
                                    **headers)
        ticket = json.loads(response.content)
        ticketid = ticket["id"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ticket["title"], payload["title"])
        self.assertEqual(ticket["description"], payload["description"])
        # Get Ticket
        response = self.client.get(
            reverse("tickets:ticket", kwargs={"pk": ticketid}), **headers)
        ticket = json.loads(response.content)
        self.assertEqual(ticket["title"], payload["title"])
        self.assertEqual(ticket["description"], payload["description"])

    def test_create_ticket_wrong_board(self):
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        username2 = "Tom--"
        password2 = "123"
        (response, created_user) = self.create_user(username2, password2)
        (response, data) = self.get_token(username2, password2)
        token2 = data["token"]
        headers2 = {"HTTP_AUTHORIZATION": "Token " + token2}
        # Create board
        name = "Board Name for tickets"
        (response, created_board) = self.create_board(name, headers=headers)
        self.assertEqual(response.status_code, 201)
        boardid = created_board["id"]
        # Create ticket
        payload = {
            "title": "Ticket Title",
            "description": "Ticket Description",
            "board": boardid,
        }
        response = self.client.post(reverse("tickets:tickets"),
                                    json.dumps(payload),
                                    content_type="application/json",
                                    **headers2)
        error = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(error["error"], "You don't have access to the board")

    def test_create_and_ticket_list(self):
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        # Get token
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        # Create board
        name = "Board Name for tickets"
        (response, created_board) = self.create_board(name, headers=headers)
        self.assertEqual(response.status_code, 201)
        boardid = created_board["id"]
        # Create ticket
        created_tickets = []
        number_of_tickets = 5
        for n in range(number_of_tickets):
            payload = {
                "title": "Ticket Title" + str(n),
                "description": "Ticket Description" + str(n),
                "board": boardid,
            }
            response = self.client.post(reverse("tickets:tickets"),
                                        json.dumps(payload),
                                        content_type="application/json",
                                        **headers)
            ticket_created = json.loads(response.content)
            created_tickets.append((response, ticket_created))
        url = reverse("tickets:tickets") + "?boardid=" + str(boardid)
        response = self.client.get(url, **headers)
        tickets = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(tickets), number_of_tickets)
        for n in range(number_of_tickets):
            self.assertIn(created_tickets[n][1], tickets)

    def test_update_ticket(self):
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        # Create board
        name = "Board Name for tickets"
        (response, created_board) = self.create_board(name, headers=headers)
        boardid = created_board["id"]
        # Create ticket
        payload = {
            "title": "Ticket Title",
            "description": "Ticket Description",
            "board": boardid,
        }
        response = self.client.post(reverse("tickets:tickets"),
                                    json.dumps(payload),
                                    content_type="application/json",
                                    **headers)
        ticket = json.loads(response.content)
        ticketid = ticket["id"]
        # Update Ticket
        newTitle = "New title"
        newDescription = "New description"
        payload = {
            "title": newTitle,
            "description": newDescription,
        }
        response = self.client.patch(reverse("tickets:ticket",
                                             kwargs={"pk": ticketid}),
                                     payload,
                                     content_type="application/json",
                                     **headers)
        ticket = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ticket["title"], payload["title"])
        self.assertEqual(ticket["description"], payload["description"])
        # Get Ticket
        response = self.client.get(
            reverse("tickets:ticket", kwargs={"pk": ticketid}), **headers)
        ticket = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ticket["title"], payload["title"])
        self.assertEqual(ticket["description"], payload["description"])

    def test_delete_ticket(self):
        # Create user
        username = "Tom"
        password = "123"
        (response, created_user) = self.create_user(username, password)
        (response, data) = self.get_token(username, password)
        token = data["token"]
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        # Create board
        name = "Board Name for tickets"
        (response, created_board) = self.create_board(name, headers=headers)
        boardid = created_board["id"]
        # Create ticket
        payload = {
            "title": "Ticket Title",
            "description": "Ticket Description",
            "board": boardid,
        }
        response = self.client.post(reverse("tickets:tickets"),
                                    json.dumps(payload),
                                    content_type="application/json",
                                    **headers)
        ticket = json.loads(response.content)
        ticketid = ticket["id"]
        # Delete Ticket
        response = self.client.delete(
            reverse("tickets:ticket", kwargs={"pk": ticketid}), **headers)
        ticket = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ticket["title"], payload["title"])
        self.assertEqual(ticket["description"], payload["description"])
        # Get Ticket
        response = self.client.get(
            reverse("tickets:ticket", kwargs={"pk": ticketid}), **headers)
        ticket = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
