"""
Test for models
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


class ModelTest(TestCase):
    """ Test models"""

    def test_create_user_with_email_successful(self):

        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@Example.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_user_without_email_raises_error(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_super_user(self):

        user = get_user_model().objects.create_superuser(
            email='test.example.com',
            password='test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a receipe is successful."""
        user = get_user_model().objects.create_superuser(
            email='test.example.com',
            password='test123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Receipe Name',
            time_minutes=5,
            price=Decimal('5'),
            description='Sample Recipe Description'
        )

        self.assertEqual(str(recipe), recipe.title)
