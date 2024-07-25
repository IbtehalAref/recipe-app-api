"""
Tests for the user API.
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'example1@test.com',
            'password': 'test1234',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        print(payload['password'])
        # self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_with_email_exists(self):
        """Test error is returned if user with already existing email exists. """
        payload = {
            'email': 'example@test.com',
            'password': 'test123',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test error is returned ifthe password is less than 5 chars. """
        payload = {
            'email': 'example@test.com',
            'password': '1',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_the_user(self):
        """test create a token for a valid credentials"""

        user_detail = {
            'email': 'example@test.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        create_user(**user_detail)

        payload = {
            'email': user_detail['email'],
            'password': user_detail['password']

        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """test returns error if credentials is invalid."""

        user_detail = {
            'email': 'example@test.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        create_user(**user_detail)

        payload = {
            'email': user_detail['email'],
            'password': 'pass123'

        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """test posting a blank password returns error"""

        payload = {
            'email': 'example@test.com',
            'password': ''

        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
