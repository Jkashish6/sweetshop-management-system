import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import CustomUser
from api.models import Sweet

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


@pytest.mark.django_db
def test_get_all_sweets_returns_list():
    # Setup: create a user and authenticate
    user = CustomUser.objects.create_user(
        username="testuser",
        password="strongpassword123",
        email="test@example.com"
    )

    client = APIClient()

    # Get JWT token
    login_response = client.post(reverse("user-login"), {
        "username": "testuser",
        "password": "strongpassword123"
    }, format="json")

    access_token = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Create some sweets
    Sweet.objects.create(name="Ladoo", category="Indian", price=10.5, quantity=100)
    Sweet.objects.create(name="Barfi", category="Indian", price=15.0, quantity=50)

    url = reverse("sweet-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Ladoo"
    assert response.data[1]["name"] == "Barfi"

@pytest.mark.django_db
def test_create_sweet_authenticated_user_can_add_sweet():
    # Create user
    user = CustomUser.objects.create_user(
        username="sweetadmin",
        password="adminpass123",
        email="admin@example.com"
    )

    client = APIClient()

    # Login to get JWT token
    login_response = client.post(reverse("user-login"), {
        "username": "sweetadmin",
        "password": "adminpass123"
    }, format="json")

    access_token = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Prepare sweet data
    sweet_data = {
        "name": "Rasgulla",
        "category": "Bengali",
        "price": 25.0,
        "quantity": 70
    }

    url = reverse("create-sweet")
    response = client.post(url, sweet_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Rasgulla"
    assert Sweet.objects.count() == 1