from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from hotels.models import Hotel
from users.models import User
from users.authentication import UserTokenAuthentication


class HotelAPITestCase(APITestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="A test hotel",
            price=100.00,
            location="Test City",
            amenities="WiFi, Pool",
            is_active=True,
        )
        self.admin = User.objects.create(
            full_name="Admin",
            email="admin@example.com",
            phone="0123",
            address="HN",
            role="admin",
            password="",
            is_active=True,
        )
        self.admin.set_password("adminpass")
        self.admin.save()
        self.admin_token = UserTokenAuthentication.issue_token(self.admin)

    def auth_headers(self, token):
        return {"HTTP_AUTHORIZATION": f"Token {token.key}"}

    def test_get_hotels_list(self):
        url = reverse("api:hotel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_hotel_detail(self):
        url = reverse("api:hotel-detail", args=[self.hotel.hotel_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Hotel")

    def test_create_hotel_requires_auth(self):
        url = reverse("api:hotel-list")
        data = {
            "name": "New Hotel",
            "description": "New hotel description",
            "price": 150.00,
            "location": "New City",
            "amenities": "WiFi, Gym",
            "is_active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_hotel_as_admin(self):
        url = reverse("api:hotel-list")
        data = {
            "name": "Admin Hotel",
            "description": "Created by admin",
            "price": 200.00,
            "location": "Admin City",
            "amenities": "Pool",
            "is_active": True,
        }
        response = self.client.post(url, data, **self.auth_headers(self.admin_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hotel.objects.count(), 2)
