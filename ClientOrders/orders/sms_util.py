import africastalking
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Africastalking SDK
username = "sandbox"  # Replace with your Africastalking username
api_key = "atsk_d2b4ce22879abe8bbe11b10bd90910d249dcdfaeca69efbbb6b8d25f6d7771ffdbdb24ba"  # Replace with your Africastalking API key

africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_sms(phone_number, message):
    logging.info(f"Attempting to send SMS to {phone_number}")
    try:
        response = sms.send(message, [phone_number])
        logging.info(f"SMS sent successfully. Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Failed to send SMS to {phone_number}: {e}")
        return None

# Example usage

