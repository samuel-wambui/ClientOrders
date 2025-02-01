from rest_framework import viewsets, status
from rest_framework.response import Response
from orders.models import Customer, Order
from orders.serializable import CustomerSerializer, OrderSerializer
from orders.sms_util import send_sms  # Ensure correct import path for send_sms

def format_phone_number(phone):
    """
    Format the phone number as follows:
      - If it starts with '+254', leave it as is.
      - If it starts with '254', add a leading '+'.
      - If it starts with '0', remove the '0' and prepend '+254'.
      - Otherwise, prepend '+254'.
    """
    phone = phone.strip()  # Remove any leading/trailing whitespace
    if phone.startswith('+254'):
        return phone
    elif phone.startswith('254'):
        return '+' + phone
    elif phone.startswith('0'):
        return '+254' + phone[1:]
    else:
        return '+254' + phone

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to send an SMS after creating an order.
        Before sending SMS, format the customer's phone number:
          - If the number starts with '0', remove the '0' and add '+254'
          - If the number does not start with '+254', add '+254'
          - If the number starts with '254', add a '+' in front.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order = serializer.instance
        customer = order.customer

        # Format the customer's phone number before sending the SMS
        formatted_phone = format_phone_number(customer.phone_number)
        # Update the customer's phone number if it differs from the current value
        if customer.phone_number != formatted_phone:
            customer.phone_number = formatted_phone
            customer.save()

        # Prepare the SMS message
        message = (
            f"Dear {customer.name}, your order for {order.item} has been placed successfully. "
            f"Total: {order.amount:.2f}."
        )
        try:
            sms_response = send_sms(formatted_phone, message)
            sms_status = sms_response["SMSMessageData"]["Recipients"][0]["status"]
        except Exception as e:
            sms_status = f"Failed: {e}"

        # Prepare and return the custom response
        response_data = {
            "message": f"Order for {order.item} created successfully.",
            "sms_status": sms_status,
            "data": serializer.data,
        }
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
