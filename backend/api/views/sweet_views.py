from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from api.models import Sweet
from api.serializers.sweet_serializers import SweetSerializer

class SweetListCreateView(ListCreateAPIView):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer
    permission_classes = [IsAuthenticated]
