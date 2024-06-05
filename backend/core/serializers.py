from rest_framework import serializers
from core.models import Word
from .models import ProductDetails


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