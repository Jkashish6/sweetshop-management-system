from django.urls import path
from api.views.sweet_views import SweetListCreateView

urlpatterns = [
    path('sweets/', SweetListCreateView.as_view(), name="sweet-list"),
]
