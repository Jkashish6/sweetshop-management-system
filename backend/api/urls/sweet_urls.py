from django.urls import path
from api.views.sweet_views import SweetListCreateView
from api.views.sweet_views import SweetDetailView
from api.views.sweet_views import sweet_search_view

urlpatterns = [
    path('sweets/', SweetListCreateView.as_view(), name="sweet-list"),
    path('sweets/<int:pk>/', SweetDetailView.as_view(), name="sweet-detail"),
    path('sweets/search/', sweet_search_view, name='sweet-search'),
]
