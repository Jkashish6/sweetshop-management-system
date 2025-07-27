# api/serializers/sweet_serializers.py
from rest_framework import serializers
from api.models import Sweet

class SweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sweet
        fields = ['id', 'name', 'category', 'price', 'quantity']
