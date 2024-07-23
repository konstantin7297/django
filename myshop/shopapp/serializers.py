from typing import Dict, List

from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(method_name='get_image')
    subcategories = serializers.SerializerMethodField(method_name='get_subcategories')

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    def get_image(self, obj: Category) -> Dict:
        if obj.image:
            return {"src": obj.image.url, "alt": obj.image.alt}
        else:
            return {}

    def get_subcategories(self, obj: Category) -> List:
        if obj.subcategories:
            return [CategorySerializer(cat).data for cat in obj.subcategories.all()]
        else:
            return []


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    tags = serializers.SerializerMethodField(method_name='get_tags')

    class Meta:
        model = Product
        fields = (
            "id", "category", "price", "count", "date", "title", "description",
            "freeDelivery", "images", "tags", "reviews", "rating"
        )

    def get_images(self, obj: Product) -> List:
        if obj.images:
            return [{"src": img.image.url, "alt": img.image.name} for img in obj.images.all()]
        else:
            return []

    def get_tags(self, obj: Product) -> List:
        if obj.tags:
            return [{"id": tag.pk, "name": tag.name} for tag in obj.tags.all()]
        else:
            return []
