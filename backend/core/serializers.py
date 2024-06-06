from rest_framework import serializers
from core.models import Word
from .models import ProductDetails
from .models import RequestDetails

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['word']

class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

class ImageSerializer1(serializers.Serializer):
    image = serializers.ImageField()

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = '__all__'



class RequestDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDetails
        fields = '__all__'
        resource_name = 'requestDetails'  # Ensure the resource name is defined

# class RequestDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RequestDetails
#         # resource_name = 'requestDetails'
#         fields = '__all__'