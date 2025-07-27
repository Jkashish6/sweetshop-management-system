from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from api.models import Sweet
from api.serializers.sweet_serializers import SweetSerializer
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes


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

class SweetDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)
        serializer = SweetSerializer(sweet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)
        serializer = SweetSerializer(sweet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)
        sweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def sweet_search_view(request):
    name = request.GET.get("name", "")
    category = request.GET.get("category", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    sweets = Sweet.objects.all()

    if name:
        sweets = sweets.filter(name__icontains=name)
    if category:
        sweets = sweets.filter(category__icontains=category)
    if min_price:
        sweets = sweets.filter(price__gte=min_price)
    if max_price:
        sweets = sweets.filter(price__lte=max_price)

    serializer = SweetSerializer(sweets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class SweetPurchaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)
        quantity = request.data.get("quantity")

        if not quantity or not str(quantity).isdigit() or int(quantity) <= 0:
            return Response({"error": "Quantity must be a positive integer"}, status=400)

        quantity = int(quantity)
        if sweet.quantity < quantity:
            return Response({"error": "Not enough stock"}, status=400)

        sweet.quantity -= quantity
        sweet.save()
        return Response({"message": "Sweet purchased successfully", "remaining_quantity": sweet.quantity}, status=200)


class SweetRestockView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Admin only endpoint"}, status=403)

        sweet = get_object_or_404(Sweet, pk=pk)
        quantity = request.data.get("quantity")

        if not quantity or not str(quantity).isdigit() or int(quantity) <= 0:
            return Response({"error": "Quantity must be a positive integer"}, status=400)

        sweet.quantity += int(quantity)
        sweet.save()
        return Response({"message": "Sweet restocked successfully", "updated_quantity": sweet.quantity}, status=200)
