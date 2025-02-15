Customer and Order Management System with OIDC Authentication and Africa's Talking Integration

Project Description

This is a Django-based application for managing customers and orders. It features OIDC (OpenID Connect) authentication for secure login and integrates Africa's Talking API for SMS notifications. The system enables users to authenticate via OIDC, manage customer data, place orders, and receive order updates via SMS.

Key Features

OIDC Authentication: Secure authentication via OpenID Connect.

Order Management: manage customer orders.

Customer Management: Maintain customer profiles and contact details.

Africa's Talking SMS Integration: Send SMS notifications for order updates.

API Endpoints: Well-structured REST API for customer and order management.

Continuous Integration/Continuous Deployment (CI/CD): Automated testing and deployment workflow.

Test Coverage: Comprehensive test coverage with automated checks.

Deployed on Heroku: Accessible at Client Orders on Heroku.

Prerequisites

Before running the project, ensure you have the following installed:

Python 3.x

Django 4.x

pip (Python package manager)

Africa's Talking API credentials (for SMS integration)

OIDC credentials for authentication

Installation Instructions

Clone the repository:

git clone https://github.com/samuel-wambui/ClientOrders.git
cd clientorders

Set up a virtual environment:

python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate  # For Windows

Install dependencies:

pip install -r requirements.txt

Run database migrations:

python manage.py migrate

Run tests and measure coverage:

coverage run --source=Authorization,orders manage.py test
coverage report --fail-under=80

Start the development server:

python manage.py runserver

The server will be accessible at http://127.0.0.1:8000.

API Usage

Testing API Endpoints

Use Postman or Google Chrome to test the API endpoints.

Example: To authenticate a user via OIDC, send a POST request to:

http://127.0.0.1:8000/auth/token/

with the necessary OIDC parameters.

Available Endpoints

POST /oidc/authenticate/ - Authenticate a user via OIDC.

GET /customers/ - List all customers.

POST /customers/ - Create a new customer.

GET /orders/ - Retrieve all orders.

POST /orders/ - Place a new order (triggers an SMS notification via Africa's Talking).

Deployment & CI/CD

CI/CD Pipeline: Automated testing and deployment process ensures code quality.

Deployed on Heroku: Access the live system at Client Orders on Heroku.

Test Coverage: The system ensures a minimum of 80% test coverage.

License

This project is licensed under the MIT License - see the LICENSE file for details.