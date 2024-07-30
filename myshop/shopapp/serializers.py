from typing import Dict, List

from rest_framework import serializers

from .models import Category, Tag, Product, Review, Order


class SideCategorySerializer(serializers.ModelSerializer):
    """ Side serializer for category model """
    image = serializers.SerializerMethodField(method_name='get_image')

    class Meta:
        model = Category
        fields = ("id", "title", "image")

    @staticmethod
    def get_image(obj: Category) -> Dict:
        return {"src": obj.image.url, "alt": obj.image.name} if obj.image else {}


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for category model """
    image = serializers.SerializerMethodField(method_name='get_image')
    subcategories = serializers.SerializerMethodField(method_name='get_subcategories')

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    @staticmethod
    def get_image(obj: Category) -> Dict:
        return {"src": obj.image.url, "alt": obj.image.name} if obj.image else {}

    @staticmethod
    def get_subcategories(obj: Category) -> List:
        return SideCategorySerializer(
            obj.subcategories.all(), many=True
        ).data if obj.subcategories else []


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tag model """
    class Meta:
        model = Tag
        fields = ("id", "name")


class ShortProductSerializer(serializers.ModelSerializer):
    """ Serializer for short product model """
    price = serializers.SerializerMethodField(method_name='get_price')
    date = serializers.SerializerMethodField(method_name='get_date')
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
    def get_price(obj: Product) -> float:
        return float(obj.price) if obj.price else 0

    @staticmethod
    def get_date(obj: Product) -> str:
        return obj.date.strftime("%a %b %d %Y %H:%M:%S %z %Z")

    @staticmethod
    def get_images(obj: Product) -> List:
        return [
            {"src": img.image.url, "alt": img.image.name} for img in obj.images.all()
        ] if obj.images else []

    @staticmethod
    def get_tags(obj: Product) -> List:
        return [
            {"id": tag.pk, "name": tag.name} for tag in obj.tags.all()
        ] if obj.tags else []

    @staticmethod
    def get_reviews(obj: Product) -> int:
        return len(obj.reviews.all())


class FullProductSerializer(serializers.ModelSerializer):
    """ Serializer for full product model """
    price = serializers.SerializerMethodField(method_name='get_price')
    date = serializers.SerializerMethodField(method_name='get_date')
    category = serializers.SerializerMethodField(method_name='get_category')
    images = serializers.SerializerMethodField(method_name='get_images')
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')

    class Meta:
        model = Product
        fields = (
            "id", "category", "price", "count", "date", "title", "description",
            "fullDescription", "freeDelivery", "images", "tags", "reviews",
            "specifications", "rating"
        )

    @staticmethod
    def get_price(obj: Product) -> float:
        return float(obj.price) if obj.price else 0

    @staticmethod
    def get_date(obj: Product) -> str:
        return obj.date.strftime("%a %b %d %Y %H:%M:%S %z %Z")

    @staticmethod
    def get_category(obj: Product) -> int | None:
        return int(obj.category.id) if obj.category else None

    @staticmethod
    def get_images(obj: Product) -> List:
        return [
            {"src": img.image.url, "alt": img.image.name} for img in obj.images.all()
        ] if obj.images else []

    @staticmethod
    def get_tags(obj: Product) -> List:
        return TagSerializer(obj.tags.all(), many=True).data if obj.tags else []

    @staticmethod
    def get_reviews(obj: Product) -> List:
        return ReviewSerializer(
            obj.reviews.all(), many=True
        ).data if obj.reviews else []

    @staticmethod
    def get_specifications(obj: Product) -> List:
        return [
            {"name": spec.name, "value": spec.value}
            for spec in obj.specifications.all()
        ] if obj.specifications else []


class ReviewSerializer(serializers.ModelSerializer):
    """ Serializer for review model """
    date = serializers.SerializerMethodField(method_name='get_date')

    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date")

    @staticmethod
    def get_date(obj: Review) -> str:
        return obj.date.strftime("%Y-%m-%d %H:%M")


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for order model """
    createdAt = serializers.SerializerMethodField(method_name='get_date')
    products = serializers.SerializerMethodField(method_name='get_products')

    class Meta:
        model = Order
        fields = "__all__"

    @staticmethod
    def get_date(obj: Order) -> str:
        return obj.createdAt.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def get_products(obj: Order) -> List:
        return ShortProductSerializer(
            obj.products.all(), many=True
        ).data if obj.products else []
