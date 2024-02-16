from scraperapp.models import Product

from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    category = serializers.CharField()
    duration = serializers.IntegerField()
    products_number = serializers.IntegerField()
    url = serializers.URLField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
