from typing import Dict, List

from rest_framework import serializers

from .models import Category, Tag, Product, Review, Order


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for category model """
    image = serializers.SerializerMethodField(method_name='get_image')
    subcategories = serializers.SerializerMethodField(method_name='get_subcategories')

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    @staticmethod
    def get_image(obj: Category) -> Dict:
        if obj.image:
            return {"src": obj.image.url, "alt": obj.image.name}
        else:
            return {}

    @staticmethod
    def get_subcategories(obj: Category) -> List:
        if obj.subcategories:
            return [CategorySerializer(cat).data for cat in obj.subcategories.all()]
        else:
            return []


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tag model """
    class Meta:
        model = Tag
        fields = ("id", "name")


class FullProductSerializer(serializers.ModelSerializer):
    """ Serializer for full product model """
    category = serializers.SerializerMethodField(method_name='get_category')
    images = serializers.SerializerMethodField(method_name='get_images')
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')

    class Meta:
        model = Product
        fields = "__all__"

    @staticmethod
    def get_category(obj: Product) -> int:
        return obj.category.id

    @staticmethod
    def get_images(obj: Product) -> List:
        return [{"src": img.image.url, "alt": img.image.name} for img in obj.images.all()]

    @staticmethod
    def get_tags(obj: Product) -> List:
        return [tag.name for tag in obj.tags.all()]

    @staticmethod
    def get_reviews(obj: Product) -> List:
        return [{
            "author": review.author,
            "email": review.email,
            "text": review.text,
            "rate": review.rate,
            "date": review.date,
        } for review in obj.reviews.all()]

    @staticmethod
    def get_specifications(obj: Product) -> List:
        return [{"name": spec.name, "value": spec.value} for spec in obj.specifications.all()]


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer for short product model """
    price = serializers.SerializerMethodField(method_name='get_price')
    images = serializers.SerializerMethodField(method_name='get_images')
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')

    class Meta:
        model = Product
        fields = (
            "id", "category", "price", "count", "date", "title", "description",
            "freeDelivery", "images", "tags", "reviews", "rating"
        )

    @staticmethod
    def get_price(obj) -> float:
        return float(obj.price)

    @staticmethod
    def get_images(obj: Product) -> List:
        if obj.images:
            return [{"src": img.image.url, "alt": img.image.name} for img in obj.images.all()]
        else:
            return []

    @staticmethod
    def get_tags(obj: Product) -> List:
        if obj.tags:
            return [{"id": tag.pk, "name": tag.name} for tag in obj.tags.all()]
        else:
            return []

    @staticmethod
    def get_reviews(obj: Product) -> int:
        return len(obj.reviews.all())


class ReviewSerializer(serializers.ModelSerializer):
    """ Serializer for review model """
    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date")


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for order model """
    products = serializers.SerializerMethodField(method_name='get_products')

    class Meta:
        model = Order
        fields = "__all__"

    @staticmethod
    def get_products(obj: Order) -> List:
        return [ProductSerializer(product).data for product in obj.products.all()]
