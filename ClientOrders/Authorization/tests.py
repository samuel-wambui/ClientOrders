from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from unittest.mock import patch
from Authorization.views import jwt_login_view, upgrade_user_to_admin  # Import your views
from django.urls import reverse
from django.http import Http404
from Authorization.models import Role

class JWTLoginTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.User = get_user_model()

    @patch('Authorization.views.decode_jwt_and_get_email')  # Mock the JWT decoder
    def test_user_registration_and_role_assignment(self, mock_decode_jwt):
        mock_email = "testuser@example.com"
        mock_decode_jwt.return_value = mock_email  # Simulate a decoded email

        request = self.factory.post("/jwt-login/", HTTP_AUTHORIZATION="Bearer mocktoken")
        response = jwt_login_view(request)

        self.assertEqual(response.status_code, 200)  # Check if request succeeds
        self.assertTrue(self.User.objects.filter(email=mock_email).exists())  # Check if user is created


class UpgradeUserToAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.User = get_user_model()
        self.user = self.User.objects.create(email="testuser@example.com")


def test_upgrade_user_to_admin_success(self):
    """Test upgrading a user to admin successfully."""
    admin_role, _ = Role.objects.get_or_create(name="admin")  # Ensure role exists

    request = self.factory.post(reverse('upgrade_user_to_admin', args=[self.user.email]))  # Simulate request
    response = upgrade_user_to_admin(request, self.user.email)

    response_data = response.json()  # Extract JSON data
    self.assertEqual(response.status_code, 200)
    self.assertIn("upgraded to admin", response_data["message"])
    self.assertTrue(self.user.roles.filter(name="admin").exists())  # Check role assigned
    self.user.refresh_from_db()
    self.assertTrue(self.user.is_staff)  # Ensure is_staff is True

def test_user_already_admin(self):
    """Test that if a user is already an admin, no changes occur."""
    admin_role, _ = Role.objects.get_or_create(name="admin")
    self.user.roles.add(admin_role)  # Assign admin role before test
    self.user.save()

    request = self.factory.post(reverse('upgrade_user_to_admin', args=[self.user.email]))
    response = upgrade_user_to_admin(request, self.user.email)

    response_data = response.json()  # Extract JSON data
    self.assertEqual(response.status_code, 200)
    self.assertIn("already an admin", response_data["message"])
from django.test import TestCase

# Create your tests here.
