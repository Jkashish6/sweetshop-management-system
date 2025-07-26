import pytest
from rest_framework.test import APIClient
from django.urls import reverse

client = APIClient()

@pytest.mark.django_db
def test_user_registration():
    url = reverse("user-register")
    data = {
        "username": "kashish",
        "email": "kashish@example.com",
        "first_name": "Kashish",
        "last_name": "Jobaliya",
        "password": "strongpass123"
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data["message"] == "User registered successfully."

