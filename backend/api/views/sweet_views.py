from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from api.models import Sweet
from api.serializers.sweet_serializers import SweetSerializer


class SweetListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sweets = Sweet.objects.all()
        serializer = SweetSerializer(sweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

