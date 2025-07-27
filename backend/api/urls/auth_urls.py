from django.urls import path
from api.views.auth_views import RegisterView
from api.views.auth_views import LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
]