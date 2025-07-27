from django.urls import path
from api.views.sweet_views import SweetListCreateView
from api.views.sweet_views import SweetDetailView

urlpatterns = [
    path('sweets/', SweetListCreateView.as_view(), name="sweet-list"),
    path('sweets/<int:pk>/', SweetDetailView.as_view(), name="sweet-detail"),
]
