from django.urls import path
from api.views.auth_views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
]