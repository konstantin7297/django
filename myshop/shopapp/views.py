from decimal import Decimal
from math import ceil

from django.db import transaction
from django.db.models import Q, Avg
from django.http import HttpRequest
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ReviewForm
from .models import Category, Tag, Product, Review, Order
from .serializers import (
    CategorySerializer,
    TagSerializer,
    FullProductSerializer,
    ReviewSerializer,
    ProductSerializer,
    OrderSerializer,
)


class CategoriesView(ListAPIView):
    """ View for listing all categories """
    queryset = Category.objects.prefetch_related("subcategories")
    serializer_class = CategorySerializer


class CatalogView(ListAPIView):
    """ View for listing filtered products """
    queryset = Product.objects.prefetch_related("tags", "images").select_related("category")

    def get(self, request: Request, *args, **kwargs):
        data = request.query_params.dict()
        page = int(data.get("currentPage", 1))
        limit = int(data.get("limit", 20))
        start_row = max((page - 1) * limit, 1)
        end_row = page * limit + 1

        result = self.get_queryset().filter(
            Q(name__icontains=data.get('filter[name]')) if data.get('filter[name]') else Q(),
            price__gte=Decimal(data.get('filter[minPrice]', 0)),
            price__lte=Decimal(data.get('filter[maxPrice]', 9999999999)),
            freeDelivery=bool(data.get('filter[freeDelivery]', "false").capitalize()),
            count__gt=0 if bool(data.get('filter[available]', "true").capitalize()) else Q(),
        ).order_by('price' if data.get('sortType', "dec") == 'inc' else '-price')[start_row:end_row]

        return Response({
            "items": ProductSerializer(result, many=True).data,
            "currentPage": page,
            "lastPage": ceil(len(result) / limit)
        })


# class ProductsPopularView(ListAPIView):
#     """В каталог топ-товаров попадают восемь первых товаров по параметру «индекс
#     сортировки». Если же индекс сортировки совпадает, то товары сортируются
#     по количеству покупок."""
#     queryset = Product.objects.prefetch_related("tags", "images").select_related("category")[:8]
#     # serializer_class = ProductSerializer


class ProductsLimitedView(ListAPIView):
    queryset = Product.objects.prefetch_related(
        "tags", "images"
    ).select_related("category").filter(limited=True)[:16]
    serializer_class = ProductSerializer


class ProductReviewView(APIView):
    """ View for posting reviews for a product """
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get("id"))
        data = request.data
        data["product"] = product

        form = ReviewForm(data=data)
        if form.is_valid():
            form.save()

            rating = product.reviews.aggregate(Avg("rate"))
            product.rating = round(rating["rate__avg"], 1)
            product.save()

            return Response(ReviewSerializer(
                Review.objects.filter(product__id=kwargs.get("id")), many=True
            ).data)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductByIdView(APIView):
    """ View for getting a full product information by id """
    def get(self, request, *args, **kwargs):
        product = Product.objects.prefetch_related(
            "images", "tags", "reviews", "specifications"
        ).get(pk=kwargs.get("id"))
        return Response(FullProductSerializer(product).data)


class OrdersView(APIView):
    """ View for main operation with orders """
    def get(self, request, *args, **kwargs):
        orders = Order.objects.prefetch_related("products").all()
        return Response(OrderSerializer(orders, many=True).data)

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        order = Order.objects.create()
        order.save()
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            print(1, serializer.validated_data)  # [{'category': <Category: Category: 'Category3'>, 'count': 50, 'date': datetime.datetime(2024, 7, 24, 6, 57, 59, 944237, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'title': 'Product8', 'description': 'Description8', 'freeDelivery': True, 'rating': 1.0}]
            for product in serializer.validated_data:
                print(2, product)  # Получаем словарь с данными продукта после десериализации, тут уже не хватает цены, картинок...
                order.products.add(Product(**product))  # ValueError: Cannot add "<Product: Product: 'Product8'>": the value for field "product" is None
            return Response({"orderId": order.id})
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrdersByIdView(APIView):
    """ View for getting and updating orders by id """
    def get(self, request, *args, **kwargs):
        order = Order.objects.prefetch_related("products").get(pk=kwargs.get("id"))
        return Response(OrderSerializer(order).data)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs.get("id"))
        data = request.data
        serializer = OrderSerializer(data=data, instance=order)

        if serializer.is_valid():
            serializer.update(order, serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class SalesView(ListAPIView):
#     pass


# class BannersView(ListAPIView):
#     pass


# class BasketView(APIView):
#     def get(self, request, *args, **kwargs):
#         pass
#
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         pass
#
#     @transaction.atomic
#     def delete(self, request, *args, **kwargs):
#         pass


class TagsView(ListAPIView):
    """ View for listing all tags by category """
    queryset = Tag.objects

    def get(self, request, *args, **kwargs):
        category = request.query_params.dict().get("category")
        if category:
            return Response(TagSerializer(
                self.get_queryset().filter(category__id=category), many=True
            ).data)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
