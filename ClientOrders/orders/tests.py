from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from orders.models import Customer, Order

User = get_user_model()


class OrderModelTest(TestCase):
    @patch("orders.models.send_sms")
    def test_sms_sent_on_order_creation(self, mock_send_sms):
        """
        Test that when a new Order is saved (via the model’s save method),
        the send_sms function is called with the correct arguments.
        """
        customer = Customer.objects.create(
            name="John Doe",
            code="JD123",
            phone_number="0712345678"  # Unformatted phone
        )

        order = Order.objects.create(
            item="Widget",
            amount=Decimal("99.99"),
            customer=customer,
        )

        # Ensure send_sms was called once
        mock_send_sms.assert_called_once()

        # Check message content
        args, kwargs = mock_send_sms.call_args
        sent_phone, sent_message = args
        self.assertIn("John Doe", sent_message)
        self.assertIn("Widget", sent_message)
        self.assertIn("99.99", sent_message)

    @patch("orders.models.send_sms")
    def test_sms_not_sent_on_order_update(self, mock_send_sms):
        """
        Test that send_sms is only called on order creation, not updates.
        """
        customer = Customer.objects.create(
            name="Jane Doe",
            code="JD456",
            phone_number="0711122233"
        )

        order = Order.objects.create(
            item="Gadget",
            amount=Decimal("50.00"),
            customer=customer,
        )

        # SMS should have been sent only once on creation
        mock_send_sms.assert_called_once()

        # Update order and save
        order.amount = Decimal("60.00")
        order.save()

        # Ensure no new SMS was sent
        mock_send_sms.assert_called_once()


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Authenticate user

        self.customer = Customer.objects.create(
            name="Alice Smith",
            code="AS789",
            phone_number="0712345678"
        )

    @patch("orders.views.send_sms")
    def test_create_order_sends_sms_and_formats_phone_number(self, mock_send_sms):
        """
        Test that when an order is created via the API:
          - The customer's phone number is formatted.
          - The send_sms function is called.
          - The response contains the expected SMS status and order details.
        """
        mock_send_sms.return_value = {
            "SMSMessageData": {"Recipients": [{"status": "Success"}]}
        }

        order_data = {
            "item": "Book",
            "amount": "25.50",
            "customer": self.customer.id,
        }

        url = reverse("order-list")  # Dynamically get URL

        response = self.client.post(url, order_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("sms_status", response.data)
        self.assertEqual(response.data["sms_status"], "Success")

        # Ensure SMS was sent
        mock_send_sms.assert_called_once()
        sent_phone, sent_message = mock_send_sms.call_args[0]

        self.assertTrue(sent_phone.startswith("+254"))

        # Verify phone number update
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone_number, sent_phone)

    def test_format_phone_number_function(self):
        """
        Test the standalone phone formatting function.
        """
        from orders.views import format_phone_number

        test_cases = [
            ("+254712345678", "+254712345678"),
            ("254712345678", "+254712345678"),
            ("0712345678", "+254712345678"),
            ("712345678", "+254712345678"),
            (" 0712345678 ", "+254712345678"),  # Extra whitespace
        ]

        for input_phone, expected_output in test_cases:
            self.assertEqual(format_phone_number(input_phone), expected_output)
