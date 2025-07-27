import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import CustomUser

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


@pytest.mark.django_db
def test_user_login_with_valid_credentials():
    client = APIClient()

    # Create test user
    CustomUser.objects.create_user(
        username="kashish123",
        email="kashish@example.com",
        first_name="Kashish",
        last_name="Jobaliya",
        password="securepass123"
    )

    url = reverse("user-login")
    payload = {
        "username": "kashish123",
        "password": "securepass123"
    }

    response = client.post(url, payload, format="json")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data