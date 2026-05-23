from rest_framework import serializers
from .models import Product, Category, Cart, CategoryOffer


class CategorySerializers(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model=Category
        fields='__all__'
        
class CategoryOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryOffer
        fields = '__all__'


# class ProductSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Product
#         fields='__all__'
        

class ProductSerializers(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    has_offer = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'discount_percentage',
            'discounted_price', 'has_offer', 'image', 'category'
        ]

    def get_discounted_price(self, obj):
        return obj.discounted_price()

    def get_has_offer(self, obj):
        return obj.has_offer()
