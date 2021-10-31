from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class AuthenticationTests(TestCase):
    """Test cases for authentication."""

    def setUp(self):
        super().setUp()
        self.user = {
            'username': 'Noom',
            'password': '12345678'
        }
        User.objects.create_user(**self.user)

    def test_user_log_in(self):
        response = self.client.post(reverse('login'), self.user)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('polls:index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_log_out(self):
        self.client.post(reverse('login'), self.user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.context['user'].is_authenticated)
