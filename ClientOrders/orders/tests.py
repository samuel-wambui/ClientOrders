# orders/tests.py

import json
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Customer, Order
from django.contrib.auth.models import User  # Or get_user_model() if you have a custom user model


class OrderViewSetTests(APITestCase):
    def setUp(self):
        # Create a test user and force authenticate.
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        # Create a test customer with a phone number that needs formatting.
        self.customer = Customer.objects.create(
            name='John Doe',
            phone_number='0712345678'  # Should be formatted to +254712345678
        )

        # URL for creating orders. Adjust the URL name if necessary.
        self.url = reverse('order-list')

    @patch('orders.views.send_sms')
    def test_order_creation_sends_sms_and_formats_phone(self, mock_send_sms):
        """
        Test that creating an order formats the customer's phone number,
        sends an SMS, and returns the expected response.
        """
        # Prepare the fake SMS response
        fake_sms_response = {
            "SMSMessageData": {
                "Recipients": [
                    {"status": "Success", "number": "+254712345678"}
                ]
            }
        }
        mock_send_sms.return_value = fake_sms_response

        order_data = {
            "customer": self.customer.id,
            "item": "Test Item",
            "amount": "150.50"
        }

        response = self.client.post(self.url, order_data, format='json')

        # Check that the response status is 201 CREATED.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the SMS status in the response is as expected.
        self.assertIn("sms_status", response.data)
        self.assertEqual(response.data["sms_status"], "Success")

        # Verify that the order was actually created.
        order = Order.objects.get(id=response.data["data"]["id"])
        self.assertEqual(order.item, "Test Item")
        self.assertEqual(float(order.amount), 150.50)
        self.assertEqual(order.customer, self.customer)

        # Verify that the customer's phone number was formatted.
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone_number, "+254712345678")

        # Ensure the send_sms function was called with the formatted phone and message.
        expected_message = (
            f"Dear {self.customer.name}, your order for {order.item} has been placed successfully. "
            f"Total: {order.amount:.2f}."
        )
        mock_send_sms.assert_called_once_with("+254712345678", expected_message)

    def test_order_creation_unauthenticated(self):
        """
        Test that an unauthenticated user cannot create an order.
        """
        # Remove authentication for this test.
        self.client.force_authenticate(user=None)

        order_data = {
            "customer": self.customer.id,
            "item": "Test Item",
            "amount": "150.50"
        }
        response = self.client.post(self.url, order_data, format='json')

        # Expect a 401 Unauthorized response.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomerViewSetTests(APITestCase):
    def setUp(self):
        # Create a test user and force authenticate.
        self.user = User.objects.create_user(username='testuser2', password='testpass2')
        self.client.force_authenticate(user=self.user)

        # URL for the customer list. Adjust the URL name if necessary.
        self.url = reverse('customer-list')

    def test_customer_list_authenticated(self):
        """
        Test that an authenticated user can access the customer list.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_list_unauthenticated(self):
        """
        Test that an unauthenticated user cannot access the customer list.
        """
        # Remove authentication for this test.
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
