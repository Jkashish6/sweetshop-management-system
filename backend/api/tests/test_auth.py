import pytest
from rest_framework.test import APIClient
from django.urls import reverse

client = APIClient()

@pytest.mark.django_db
def test_user_registration():
    url = reverse("user-register")
    data = {
        "username": "kashish",
        "password": "strongpass123"
    }
    response = client.post(url, data)
    assert response.status_code == 201
