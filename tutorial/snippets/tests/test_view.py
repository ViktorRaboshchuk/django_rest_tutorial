import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.test import force_authenticate

client = Client()


class SnippetsViewsTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="name", email="email@mail.com", password="Pass12345"
        )
        self.user2 = User.objects.create_user(
            username="name2", email="email@mail.com", password="Pass12345"
        )
        Snippet.objects.create(
            title="Title #1", owner=user, highlighted="Highlighted#1"
        )
        Snippet.objects.create(
            title="Title #2", owner=user, highlighted="Highlighted#2"
        )
        Snippet.objects.create(
            title="Title #3", owner=user, highlighted="Highlighted#3"
        )

        self.valid_payload = {
            "title": "title#_1",
            "code": "code#1",
            "highlighted": "highlighted#1",
        }
        self.updated_payload = {
            "title": "title#_1",
            "code": "updated_code#1",
            "highlighted": "updated_highlighted#1",
        }

    def test_get_all_snippets(self):
        response = self.client.get("/snippets/")
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_snippet(self):
        response = self.client.get("/snippets/1/")
        snippets = Snippet.objects.get(title="Title #1")
        serializer = SnippetSerializer(snippets)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method(self):
        self.assertTrue(self.client.login(username="name2", password="Pass12345"))
        response = self.client.post(
            "/snippets/",
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_method(self):
        self.assertTrue(self.client.login(username="name2", password="Pass12345"))

        response = self.client.put(
            "/snippets/1/",
            data=json.dumps(self.updated_payload),
            content_type="application/json",
        )
        resp_snip = self.client.get("/snippets/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_snip.data["code"], self.updated_payload["code"])
