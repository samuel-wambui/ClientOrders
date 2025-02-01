from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from orders.models import Customer, Order
from orders.serializable import CustomerSerializer, OrderSerializer

class OrderViewSetTest(APITestCase):
    def setUp(self):
        # Create a test customer
        self.customer = Customer.objects.create(
            name="John Doe",
            phone_number="+254745567890",
        )
        self.order_data = {
            "customer": self.customer.id,
            "item": "Test Item",
            "amount": 100.50,
        }

    @patch("myOrders.views.send_sms")
    def test_create_order_and_send_sms(self, mock_send_sms):
        # Mock the SMS sending functionality
        mock_send_sms.return_value = {
            "SMSMessageData": {
                "Recipients": [
                    {"status": "Success"}
                ]
            }
        }

        # Send a POST request to create an order
        response = self.client.post("/api/orders/", self.order_data, format="json")
        
        # Assert status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check the response data
        response_data = response.json()
        self.assertEqual(response_data["sms_status"], "Success")
        self.assertEqual(response_data["message"], "Order for Test Item created successfully.")

        # Verify the order was created in the database
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.item, "Test Item")
        self.assertEqual(order.amount, 100.50)

        # Verify the SMS function was called with correct arguments
        mock_send_sms.assert_called_once_with(
            "+254745567890", 
            "Dear John Doe, your order for Test Item has been placed successfully. Total: 100.50."
        )

    @patch("myOrders.views.send_sms")
    def test_create_order_without_sms_failure(self, mock_send_sms):
        # Simulate an error in the SMS sending
        mock_send_sms.side_effect = Exception("SMS sending failed")

        # Send a POST request to create an order
        response = self.client.post("/api/orders/", self.order_data, format="json")
        
        # Assert status code is 201 even though SMS sending failed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response data for failure in SMS sending
        response_data = response.json()
        self.assertEqual(response_data["sms_status"], "Failed: SMS sending failed")
        self.assertEqual(response_data["message"], "Order for Test Item created successfully.")

    def test_create_order_with_invalid_data(self):
        # Missing item field
        invalid_order_data = {
            "customer": self.customer.id,
            "amount": 100.50,
        }
        
        # Send a POST request to create an invalid order
        response = self.client.post("/api/orders/", invalid_order_data, format="json")

        # Assert status code is 400 for bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response data for error
        response_data = response.json()
        self.assertIn("item", response_data)  # Ensure 'item' field is required and missing
