# Authorization/tests.py

import json
from django.test import TestCase, RequestFactory
from django.http import Http404
from unittest.mock import patch
from jwt import PyJWTError
from django.contrib.auth import get_user_model

# Import the Role model and views from your Authorization app.
from Authorization.models import Role
from Authorization.views import upgrade_user_to_admin, jwt_login_view

User = get_user_model()


class UpgradeUserToAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.email = "user@example.com"
        # Create a user using the custom user model.
        self.user = User.objects.create(
            email=self.email,
            is_staff=False,
        )
        # The signal should have automatically added the default "user" role.
        # If you want to test upgrade functionality, you can start with that.
        self.user.roles.clear()  # Clear roles to simulate a user without admin privileges.
        default_role, _ = Role.objects.get_or_create(name='user')
        # You may also choose to re-add the default role if needed, e.g.:
        self.user.roles.add(default_role)

    def test_upgrade_user_to_admin_success(self):
        """
        Test that a non-admin user is upgraded: the "admin" role is added,
        the user becomes staff, and a success message is returned.
        """
        request = self.factory.get(f"/upgrade/{self.email}")
        response = upgrade_user_to_admin(request, self.email)
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {"message": f"User {self.email} upgraded to admin."})

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        admin_role = Role.objects.get(name="admin")
        self.assertIn(admin_role, self.user.roles.all())

    def test_upgrade_user_already_admin(self):
        """
        Test that if the user already has the admin role, a message indicating so is returned.
        """
        admin_role, _ = Role.objects.get_or_create(name="admin")
        self.user.roles.add(admin_role)
        self.user.is_staff = True
        self.user.save()

        request = self.factory.get(f"/upgrade/{self.email}")
        response = upgrade_user_to_admin(request, self.email)
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {"message": f"User {self.email} is already an admin."})

    def test_upgrade_nonexistent_user(self):
        """
        Test that attempting to upgrade a non-existent user raises a 404.
        """
        non_existent_email = "doesnotexist@example.com"
        request = self.factory.get(f"/upgrade/{non_existent_email}")
        with self.assertRaises(Http404):
            upgrade_user_to_admin(request, non_existent_email)


class JWTLoginViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('Authorization.views.decode_jwt_and_get_email')
    def test_jwt_login_view_success_new_user(self, mock_decode):
        """
        Test that when a valid JWT is provided and the user does not exist,
        a new user is created, assigned the default role, and a success message is returned.
        """
        test_email = "newuser@example.com"
        mock_decode.return_value = test_email

        request = self.factory.get("/jwt-login")
        response = jwt_login_view(request)
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data, {"message": f"User {test_email} authenticated and registered."}
        )

        # Verify that the user was created and has the default "user" role.
        user = User.objects.get(email=test_email)
        default_role = Role.objects.get(name="user")
        self.assertIn(default_role, user.roles.all())

    @patch('Authorization.views.decode_jwt_and_get_email')
    def test_jwt_login_view_success_existing_user(self, mock_decode):
        """
        Test that when a valid JWT is provided and the user already exists,
        the view returns a success message.
        """
        test_email = "existinguser@example.com"
        User.objects.create(email=test_email)
        mock_decode.return_value = test_email

        request = self.factory.get("/jwt-login")
        response = jwt_login_view(request)
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data, {"message": f"User {test_email} authenticated and registered."}
        )

    @patch('Authorization.views.decode_jwt_and_get_email')
    def test_jwt_login_view_jwt_error(self, mock_decode):
        """
        Test that if decode_jwt_and_get_email raises a PyJWTError,
        the view returns a 401 with an appropriate error message.
        """
        error_message = "Invalid token"
        mock_decode.side_effect = PyJWTError(error_message)

        request = self.factory.get("/jwt-login")
        response = jwt_login_view(request)
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data, {"error": error_message})

    @patch('Authorization.views.decode_jwt_and_get_email')
    def test_jwt_login_view_generic_exception(self, mock_decode):
        """
        Test that if decode_jwt_and_get_email raises a generic Exception,
        the view returns a 500 with a generic error message.
        """
        mock_decode.side_effect = Exception("Unexpected error")

        request = self.factory.get("/jwt-login")
        response = jwt_login_view(request)
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data, {"error": "Internal server error"})
