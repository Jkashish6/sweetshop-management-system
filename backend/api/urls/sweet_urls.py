# api/urls/sweet_urls.py
from django.urls import path
from api.views.sweet_views import SweetCreateView

urlpatterns = [
    path('sweets/', SweetCreateView.as_view(), name='create-sweet'),
]
