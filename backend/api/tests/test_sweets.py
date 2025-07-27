import pytest
from rest_framework.test import APIClient
from rest_framework import status
from api.models import CustomUser

@pytest.mark.django_db
def test_create_sweet_authenticated():
    # Create a user and get token
    user = CustomUser.objects.create_user(
        username="testuser", 
        email="testuser@example.com", 
        password="strongpass123"
    )

    client = APIClient()
    response = client.post('/api/auth/login/', {
        "username": "testuser",
        "password": "strongpass123"
    }, format="json")

    assert response.status_code == 200
    access_token = response.data['access']

    # Attempt to create a sweet using token
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    sweet_data = {
        "name": "Gulab Jamun",
        "category": "Dessert",
        "price": 30.5,
        "quantity": 100
    }
    res = client.post("/api/sweets/", sweet_data, format="json")
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == "Gulab Jamun"
